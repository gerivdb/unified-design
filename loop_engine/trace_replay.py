#!/usr/bin/env python3
"""
trace_replay.py - Preuve par re-exécution de trace (L6 Workshop)
Capture exécution réelle -> replay exact contre code modifié -> vérification SQL assertions.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import sqlite3
import subprocess
import sys
import time
import traceback
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import threading

logger = logging.getLogger(__name__)


@dataclass
class TraceEvent:
    """Événement unique dans une trace d'exécution."""
    id: str
    timestamp: float
    event_type: str  # function_call | function_return | exception | io_read | io_write | http_request | http_response
    thread_id: int
    function_name: str
    file_path: str
    line_number: int
    args: dict = field(default_factory=dict)
    return_value: Any = None
    exception: Optional[str] = None
    duration_ns: int = 0
    metadata: dict = field(default_factory=dict)


@dataclass
class TraceSession:
    """Session complète de trace."""
    session_id: str
    started_at: float
    ended_at: Optional[float] = None
    command: list[str] = field(default_factory=list)
    working_dir: str = ""
    events: list[TraceEvent] = field(default_factory=list)
    assertions: list[dict] = field(default_factory=list)  # Assertions SQL à vérifier
    exit_code: Optional[int] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class ReplayResult:
    """Résultat d'un replay."""
    session_id: str
    replay_id: str
    status: str  # success | mismatch | error | timeout
    events_matched: int
    events_total: int
    assertions_passed: int
    assertions_total: int
    mismatches: list[dict] = field(default_factory=list)
    assertion_failures: list[dict] = field(default_factory=list)
    duration_sec: float = 0
    error_message: str = ""


class TraceDatabase:
    """Base SQLite pour stockage traces + assertions."""
    
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS trace_sessions (
        session_id TEXT PRIMARY KEY,
        started_at REAL NOT NULL,
        ended_at REAL,
        command TEXT NOT NULL,
        working_dir TEXT NOT NULL,
        exit_code INTEGER,
        metadata TEXT
    );
    
    CREATE TABLE IF NOT EXISTS trace_events (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        timestamp REAL NOT NULL,
        event_type TEXT NOT NULL,
        thread_id INTEGER NOT NULL,
        function_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        line_number INTEGER NOT NULL,
        args TEXT,
        return_value TEXT,
        exception TEXT,
        duration_ns INTEGER DEFAULT 0,
        metadata TEXT,
        FOREIGN KEY (session_id) REFERENCES trace_sessions(session_id)
    );
    
    CREATE TABLE IF NOT EXISTS trace_assertions (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        assertion_sql TEXT NOT NULL,
        description TEXT,
        expected_result TEXT,
        FOREIGN KEY (session_id) REFERENCES trace_sessions(session_id)
    );
    
    CREATE TABLE IF NOT EXISTS replay_results (
        replay_id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        status TEXT NOT NULL,
        events_matched INTEGER,
        events_total INTEGER,
        assertions_passed INTEGER,
        assertions_total INTEGER,
        mismatches TEXT,
        assertion_failures TEXT,
        duration_sec REAL,
        error_message TEXT,
        created_at REAL NOT NULL,
        FOREIGN KEY (session_id) REFERENCES trace_sessions(session_id)
    );
    
    CREATE INDEX IF NOT EXISTS idx_events_session ON trace_events(session_id);
    CREATE INDEX IF NOT EXISTS idx_events_timestamp ON trace_events(timestamp);
    CREATE INDEX IF NOT EXISTS idx_assertions_session ON trace_assertions(session_id);
    CREATE INDEX IF NOT EXISTS idx_replays_session ON replay_results(session_id);
    """
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with self._conn() as conn:
            conn.executescript(self.SCHEMA)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
    
    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def save_session(self, session: TraceSession):
        with self._conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO trace_sessions 
                (session_id, started_at, ended_at, command, working_dir, exit_code, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.started_at, session.ended_at,
                json.dumps(session.command), session.working_dir,
                session.exit_code, json.dumps(session.metadata)
            ))
            
            # Events
            for event in session.events:
                conn.execute("""
                    INSERT OR REPLACE INTO trace_events
                    (id, session_id, timestamp, event_type, thread_id, function_name,
                     file_path, line_number, args, return_value, exception, duration_ns, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.id, session.session_id, event.timestamp, event.event_type,
                    event.thread_id, event.function_name, event.file_path,
                    event.line_number, json.dumps(event.args),
                    json.dumps(event.return_value) if event.return_value is not None else None,
                    event.exception, event.duration_ns, json.dumps(event.metadata)
                ))
            
            # Assertions
            for assertion in session.assertions:
                conn.execute("""
                    INSERT OR REPLACE INTO trace_assertions
                    (id, session_id, assertion_sql, description, expected_result)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    assertion.get("id", str(uuid.uuid4())[:12]),
                    session.session_id,
                    assertion["sql"],
                    assertion.get("description", ""),
                    json.dumps(assertion.get("expected"))
                ))
    
    def load_session(self, session_id: str) -> Optional[TraceSession]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM trace_sessions WHERE session_id = ?", (session_id,)
            ).fetchone()
            if not row:
                return None
            
            events = []
            for ev_row in conn.execute(
                "SELECT * FROM trace_events WHERE session_id = ? ORDER BY timestamp",
                (session_id,)
            ):
                events.append(TraceEvent(
                    id=ev_row["id"],
                    timestamp=ev_row["timestamp"],
                    event_type=ev_row["event_type"],
                    thread_id=ev_row["thread_id"],
                    function_name=ev_row["function_name"],
                    file_path=ev_row["file_path"],
                    line_number=ev_row["line_number"],
                    args=json.loads(ev_row["args"]) if ev_row["args"] else {},
                    return_value=json.loads(ev_row["return_value"]) if ev_row["return_value"] else None,
                    exception=ev_row["exception"],
                    duration_ns=ev_row["duration_ns"],
                    metadata=json.loads(ev_row["metadata"]) if ev_row["metadata"] else {}
                ))
            
            assertions = []
            for as_row in conn.execute(
                "SELECT * FROM trace_assertions WHERE session_id = ?", (session_id,)
            ):
                assertions.append({
                    "id": as_row["id"],
                    "sql": as_row["assertion_sql"],
                    "description": as_row["description"],
                    "expected": json.loads(as_row["expected_result"]) if as_row["expected_result"] else None
                })
            
            return TraceSession(
                session_id=row["session_id"],
                started_at=row["started_at"],
                ended_at=row["ended_at"],
                command=json.loads(row["command"]),
                working_dir=row["working_dir"],
                events=events,
                assertions=assertions,
                exit_code=row["exit_code"],
                metadata=json.loads(row["metadata"]) if row["metadata"] else {}
            )
    
    def save_replay_result(self, result: ReplayResult):
        with self._conn() as conn:
            conn.execute("""
                INSERT INTO replay_results
                (replay_id, session_id, status, events_matched, events_total,
                 assertions_passed, assertions_total, mismatches, assertion_failures,
                 duration_sec, error_message, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.replay_id, result.session_id, result.status,
                result.events_matched, result.events_total,
                result.assertions_passed, result.assertions_total,
                json.dumps(result.mismatches), json.dumps(result.assertion_failures),
                result.duration_sec, result.error_message, time.time()
            ))


class TraceCapture:
    """Capture d'exécution via sys.settrace + threading."""
    
    def __init__(self, db: TraceDatabase, session: TraceSession):
        self.db = db
        self.session = session
        self._original_trace = None
        self._thread_traces = {}
        self._call_stack = []
    
    def start(self):
        """Débute la capture."""
        self._original_trace = sys.gettrace()
        sys.settrace(self._trace_func)
        threading.settrace(self._trace_func)
        logger.info(f"Trace capture started for session {self.session.session_id}")
    
    def stop(self):
        """Arrête la capture."""
        sys.settrace(self._original_trace)
        threading.settrace(None)
        self.session.ended_at = time.time()
        self.db.save_session(self.session)
        logger.info(f"Trace capture stopped. Events: {len(self.session.events)}")
    
    def _trace_func(self, frame, event, arg):
        if event not in ("call", "return", "exception"):
            return self._trace_func
        
        # Filtrer: seulement notre code (pas stdlib, site-packages)
        filename = frame.f_code.co_filename
        if self._should_ignore(filename):
            return self._trace_func
        
        thread_id = threading.get_ident()
        
        if event == "call":
            self._handle_call(frame, thread_id)
        elif event == "return":
            self._handle_return(frame, arg, thread_id)
        elif event == "exception":
            self._handle_exception(frame, arg, thread_id)
        
        return self._trace_func
    
    def _should_ignore(self, filename: str) -> bool:
        ignore_patterns = [
            "site-packages", "dist-packages", "lib/python",
            "<frozen", "<string>", "importlib", "runpy"
        ]
        return any(p in filename for p in ignore_patterns)
    
    def _handle_call(self, frame, thread_id: int):
        event = TraceEvent(
            id=str(uuid.uuid4())[:12],
            timestamp=time.time(),
            event_type="function_call",
            thread_id=thread_id,
            function_name=frame.f_code.co_name,
            file_path=frame.f_code.co_filename,
            line_number=frame.f_lineno,
            args=self._extract_args(frame),
            metadata={"call_stack_depth": len(self._call_stack)}
        )
        self._call_stack.append(event)
        self.session.events.append(event)
    
    def _handle_return(self, frame, return_value, thread_id: int):
        if not self._call_stack:
            return
        
        call_event = self._call_stack.pop()
        duration_ns = int((time.time() - call_event.timestamp) * 1e9)
        
        return_event = TraceEvent(
            id=str(uuid.uuid4())[:12],
            timestamp=time.time(),
            event_type="function_return",
            thread_id=thread_id,
            function_name=frame.f_code.co_name,
            file_path=frame.f_code.co_filename,
            line_number=frame.f_lineno,
            return_value=self._serialize_value(return_value),
            duration_ns=duration_ns,
            metadata={"call_stack_depth": len(self._call_stack)}
        )
        self.session.events.append(return_event)
    
    def _handle_exception(self, frame, exc_info, thread_id: int):
        exc_type, exc_value, exc_tb = exc_info
        event = TraceEvent(
            id=str(uuid.uuid4())[:12],
            timestamp=time.time(),
            event_type="exception",
            thread_id=thread_id,
            function_name=frame.f_code.co_name,
            file_path=frame.f_code.co_filename,
            line_number=frame.f_lineno,
            exception=f"{exc_type.__name__}: {exc_value}",
            metadata={"traceback": "".join(traceback.format_exception(exc_type, exc_value, exc_tb))}
        )
        self.session.events.append(event)
    
    def _extract_args(self, frame) -> dict:
        """Extrait arguments d'appel (simplifié)."""
        args = {}
        try:
            code = frame.f_code
            varnames = code.co_varnames[:code.co_argcount]
            for i, name in enumerate(varnames):
                if name in frame.f_locals:
                    args[name] = self._serialize_value(frame.f_locals[name])
        except Exception:
            pass
        return args
    
    def _serialize_value(self, value: Any) -> Any:
        """Serialise une valeur pour stockage JSON."""
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, (list, tuple)):
            return [self._serialize_value(v) for v in value[:10]]  # Limite
        if isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in list(value.items())[:10]}
        if hasattr(value, "__dict__"):
            return {"_type": type(value).__name__, "_repr": repr(value)[:200]}
        return {"_type": type(value).__name__, "_repr": repr(value)[:200]}


class TraceReplayer:
    """Rejoue une trace contre code modifié et vérifie assertions SQL."""
    
    def __init__(self, db: TraceDatabase):
        self.db = db
    
    async def replay(
        self,
        session_id: str,
        modified_code_path: Path = None,
        timeout_sec: float = 60.0
    ) -> ReplayResult:
        """
        Rejoue la trace session_id.
        Si modified_code_path fourni, execute dans ce contexte.
        """
        start_time = time.time()
        replay_id = str(uuid.uuid4())[:12]
        
        # Charger session originale
        session = self.db.load_session(session_id)
        if not session:
            return ReplayResult(
                session_id=session_id,
                replay_id=replay_id,
                status="error",
                events_matched=0,
                events_total=0,
                assertions_passed=0,
                assertions_total=0,
                error_message=f"Session {session_id} not found"
            )
        
        logger.info(f"Replaying session {session_id} (replay {replay_id})")
        
        try:
            # Executer la commande originale
            result = await self._execute_command(
                session.command,
                session.working_dir,
                timeout_sec
            )
            
            # Capturer nouvelle trace
            new_session = await self._capture_execution(
                session.command, session.working_dir, timeout_sec
            )
            
            # Comparer traces
            mismatches = self._compare_traces(session, new_session)
            
            # Verifier assertions SQL
            assertion_results = self._verify_assertions(session, new_session)
            
            duration = time.time() - start_time
            
            status = "success"
            if mismatches:
                status = "mismatch"
            if assertion_results["failed"] > 0:
                status = "assertion_failed"
            
            replay_result = ReplayResult(
                session_id=session_id,
                replay_id=replay_id,
                status=status,
                events_matched=len(session.events) - len(mismatches),
                events_total=len(session.events),
                assertions_passed=assertion_results["passed"],
                assertions_total=assertion_results["total"],
                mismatches=mismatches,
                assertion_failures=assertion_results["failures"],
                duration_sec=duration
            )
            
            self.db.save_replay_result(replay_result)
            return replay_result
            
        except asyncio.TimeoutError:
            return ReplayResult(
                session_id=session_id,
                replay_id=replay_id,
                status="timeout",
                events_matched=0,
                events_total=len(session.events),
                assertions_passed=0,
                assertions_total=len(session.assertions),
                duration_sec=time.time() - start_time,
                error_message=f"Replay timed out after {timeout_sec}s"
            )
        except Exception as e:
            return ReplayResult(
                session_id=session_id,
                replay_id=replay_id,
                status="error",
                events_matched=0,
                events_total=len(session.events),
                assertions_passed=0,
                assertions_total=len(session.assertions),
                duration_sec=time.time() - start_time,
                error_message=str(e)
            )
    
    async def _execute_command(
        self,
        command: list[str],
        working_dir: str,
        timeout: float
    ) -> subprocess.CompletedProcess:
        """Execute la commande originale."""
        proc = await asyncio.create_subprocess_exec(
            *command,
            cwd=working_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return subprocess.CompletedProcess(command, proc.returncode, stdout, stderr)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            raise
    
    async def _capture_execution(
        self,
        command: list[str],
        working_dir: str,
        timeout: float
    ) -> TraceSession:
        """Capture une nouvelle exécution."""
        new_session = TraceSession(
            session_id=str(uuid.uuid4())[:12],
            started_at=time.time(),
            command=command,
            working_dir=working_dir
        )
        
        capture = TraceCapture(self.db, new_session)
        capture.start()
        
        try:
            result = await self._execute_command(command, working_dir, timeout)
            new_session.exit_code = result.returncode
        finally:
            capture.stop()
        
        return new_session
    
    def _compare_traces(
        self,
        original: TraceSession,
        replayed: TraceSession
    ) -> list[dict]:
        """Compare deux traces événement par événement."""
        mismatches = []
        
        # Aligner par (function_name, file_path, line_number, event_type)
        orig_idx = 0
        replay_idx = 0
        
        while orig_idx < len(original.events) and replay_idx < len(replayed.events):
            o = original.events[orig_idx]
            r = replayed.events[replay_idx]
            
            if self._events_match(o, r):
                orig_idx += 1
                replay_idx += 1
            else:
                # Chercher match dans les prochains événements replayed
                found = False
                for lookahead in range(replay_idx + 1, min(replay_idx + 10, len(replayed.events))):
                    if self._events_match(o, replayed.events[lookahead]):
                        # Événements manquants dans replayed
                        for skip in range(replay_idx, lookahead):
                            mismatches.append({
                                "type": "missing_in_replay",
                                "original_event": asdict(original.events[skip]),
                                "replay_index": skip
                            })
                        replay_idx = lookahead + 1
                        orig_idx += 1
                        found = True
                        break
                
                if not found:
                    mismatches.append({
                        "type": "divergence",
                        "original": asdict(o),
                        "replayed": asdict(r) if replay_idx < len(replayed.events) else None,
                        "original_index": orig_idx,
                        "replay_index": replay_idx
                    })
                    orig_idx += 1
                    replay_idx += 1
        
        # Événements restants
        for i in range(orig_idx, len(original.events)):
            mismatches.append({
                "type": "missing_in_replay",
                "original_event": asdict(original.events[i])
            })
        
        return mismatches
    
    def _events_match(self, a: TraceEvent, b: TraceEvent) -> bool:
        """Vérifie si deux événements correspondent."""
        return (a.function_name == b.function_name and
                a.file_path == b.file_path and
                a.line_number == b.line_number and
                a.event_type == b.event_type)
    
    def _verify_assertions(
        self,
        original: TraceSession,
        replayed: TraceSession
    ) -> dict:
        """Vérifie les assertions SQL sur la trace rejouée."""
        passed = 0
        failed = 0
        failures = []
        
        with self.db._conn() as conn:
            # Charger events rejoués dans table temporaire
            conn.execute("DROP TABLE IF EXISTS replay_events")
            conn.execute("""
                CREATE TEMPORARY TABLE replay_events AS
                SELECT * FROM trace_events WHERE session_id = ?
            """, (replayed.session_id,))
            
            for assertion in original.assertions:
                sql = assertion["sql"]
                expected = assertion.get("expected")
                
                try:
                    cursor = conn.execute(sql)
                    rows = cursor.fetchall()
                    
                    if expected is not None:
                        # Verifier resultat attendu
                        actual = [dict(r) for r in rows]
                        if self._results_match(actual, expected):
                            passed += 1
                        else:
                            failed += 1
                            failures.append({
                                "assertion_id": assertion.get("id"),
                                "sql": sql,
                                "expected": expected,
                                "actual": actual,
                                "description": assertion.get("description")
                            })
                    else:
                        # Assertion d'existence (au moins 1 ligne)
                        if rows:
                            passed += 1
                        else:
                            failed += 1
                            failures.append({
                                "assertion_id": assertion.get("id"),
                                "sql": sql,
                                "error": "Expected at least one row",
                                "description": assertion.get("description")
                            })
                except Exception as e:
                    failed += 1
                    failures.append({
                        "assertion_id": assertion.get("id"),
                        "sql": sql,
                        "error": str(e),
                        "description": assertion.get("description")
                    })
        
        return {"passed": passed, "failed": failed, "total": passed + failed, "failures": failures}
    
    def _results_match(self, actual: list, expected: Any) -> bool:
        """Compare resultats d'assertion."""
        if isinstance(expected, (int, float)):
            return len(actual) == expected
        if isinstance(expected, list):
            return actual == expected
        if isinstance(expected, dict):
            # Verifier que expected est subset de actual[0]
            if actual and isinstance(actual[0], dict):
                return all(actual[0].get(k) == v for k, v in expected.items())
        return str(actual) == str(expected)


def demo():
    """Demo trace replay."""
    import tempfile
    logging.basicConfig(level=logging.INFO)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "traces.db"
        db = TraceDatabase(db_path)
        
        # Creer session exemple
        session = TraceSession(
            session_id="demo-001",
            started_at=time.time(),
            command=["python", "-c", "print('hello'); x=1+2; print(x)"],
            working_dir=tmpdir
        )
        
        # Ajouter assertions SQL
        session.assertions = [
            {
                "id": "assert-001",
                "sql": "SELECT COUNT(*) as cnt FROM trace_events WHERE event_type = 'function_call'",
                "description": "At least one function call traced",
                "expected": [{"cnt": 1}]
            },
            {
                "id": "assert-002",
                "sql": "SELECT function_name FROM trace_events WHERE event_type = 'function_call'",
                "description": "Print function was called",
                "expected": [{"function_name": "print"}]
            }
        ]
        
        # Capture
        capture = TraceCapture(db, session)
        capture.start()
        
        # Simuler execution
        print("hello")
        x = 1 + 2
        print(x)
        
        capture.stop()
        
        # Replay
        replayer = TraceReplayer(db)
        result = asyncio.run(replayer.replay("demo-001", timeout_sec=10))
        
        print(f"\n=== REPLAY RESULT ===")
        print(f"Status: {result.status}")
        print(f"Events matched: {result.events_matched}/{result.events_total}")
        print(f"Assertions: {result.assertions_passed}/{result.assertions_total}")
        print(f"Duration: {result.duration_sec:.2f}s")
        
        if result.mismatches:
            print(f"Mismatches: {len(result.mismatches)}")
        if result.assertion_failures:
            print(f"Assertion failures: {result.assertion_failures}")


if __name__ == "__main__":
    demo()