#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MockPilot-CLI - Lightweight Terminal API Mock Server Intelligent Engine
轻量级终端API Mock服务器智能引擎

Zero Dependencies, Dynamic Response Generation, TUI Dashboard
零依赖、动态响应生成、TUI仪表盘

Author: MockPilot Team
License: MIT
Version: 1.0.0
"""

import sys
import os
import json
import re
import time
import random
import string
import datetime
import threading
import socket
import contextlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Any, Optional, Callable, Union

# Version info
__version__ = "1.0.0"
__author__ = "MockPilot Team"

# ANSI Colors for TUI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Mock Data Generators
class DataGenerator:
    """Generate realistic mock data"""
    
    FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", 
                   "Michael", "Linda", "William", "Elizabeth", "David", "Barbara",
                   "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah",
                   "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa"]
    
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                  "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez",
                  "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore"]
    
    DOMAINS = ["example.com", "test.org", "demo.net", "mock.io", "sample.dev"]
    
    COMPANIES = ["TechCorp", "DataSystems", "CloudNine", "InnovateLabs", 
                 "FutureTech", "SmartSolutions", "DigitalDynamics"]
    
    LOREM_WORDS = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
                   "adipiscing", "elit", "sed", "do", "eiusmod", "tempor",
                   "incididunt", "ut", "labore", "et", "dolore", "magna"]
    
    @classmethod
    def uuid(cls) -> str:
        """Generate UUID v4 format"""
        chars = string.hexdigits[:-6]
        parts = [
            ''.join(random.choices(chars, k=8)),
            ''.join(random.choices(chars, k=4)),
            '4' + ''.join(random.choices(chars, k=3)),
            hex(random.randint(8, 11))[2:] + ''.join(random.choices(chars, k=3)),
            ''.join(random.choices(chars, k=12))
        ]
        return '-'.join(parts)
    
    @classmethod
    def name(cls) -> str:
        """Generate random full name"""
        return f"{random.choice(cls.FIRST_NAMES)} {random.choice(cls.LAST_NAMES)}"
    
    @classmethod
    def email(cls) -> str:
        """Generate random email"""
        user = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
        return f"{user}@{random.choice(cls.DOMAINS)}"
    
    @classmethod
    def phone(cls) -> str:
        """Generate random phone number"""
        return f"1{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    
    @classmethod
    def company(cls) -> str:
        """Generate random company name"""
        return random.choice(cls.COMPANIES)
    
    @classmethod
    def lorem(cls, words: int = 10) -> str:
        """Generate lorem ipsum text"""
        return ' '.join(random.choices(cls.LOREM_WORDS, k=words)).capitalize() + '.'
    
    @classmethod
    def date(cls, days_offset: int = 0) -> str:
        """Generate ISO date string"""
        date = datetime.datetime.now() + datetime.timedelta(days=days_offset)
        return date.strftime("%Y-%m-%d")
    
    @classmethod
    def datetime(cls, hours_offset: int = 0) -> str:
        """Generate ISO datetime string"""
        dt = datetime.datetime.now() + datetime.timedelta(hours=hours_offset)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    @classmethod
    def boolean(cls) -> bool:
        """Generate random boolean"""
        return random.choice([True, False])
    
    @classmethod
    def integer(cls, min_val: int = 0, max_val: int = 100) -> int:
        """Generate random integer"""
        return random.randint(min_val, max_val)
    
    @classmethod
    def float_num(cls, min_val: float = 0.0, max_val: float = 100.0) -> float:
        """Generate random float"""
        return round(random.uniform(min_val, max_val), 2)
    
    @classmethod
    def choice(cls, options: List[Any]) -> Any:
        """Select random choice from list"""
        return random.choice(options)
    
    @classmethod
    def word(cls) -> str:
        """Generate random word"""
        return ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))
    
    @classmethod
    def sentence(cls, words: int = 6) -> str:
        """Generate random sentence"""
        return ' '.join([cls.word() for _ in range(words)]).capitalize() + '.'

# Template Engine
class TemplateEngine:
    """Simple template engine for dynamic response generation"""
    
    # Template patterns
    PATTERNS = {
        r'\{\{\$uuid\}\}': lambda: DataGenerator.uuid(),
        r'\{\{\$name\}\}': lambda: DataGenerator.name(),
        r'\{\{\$email\}\}': lambda: DataGenerator.email(),
        r'\{\{\$phone\}\}': lambda: DataGenerator.phone(),
        r'\{\{\$company\}\}': lambda: DataGenerator.company(),
        r'\{\{\$word\}\}': lambda: DataGenerator.word(),
        r'\{\{\$sentence\}\}': lambda: DataGenerator.sentence(),
        r'\{\{\$lorem\}\}': lambda: DataGenerator.lorem(),
        r'\{\{\$date\}\}': lambda: DataGenerator.date(),
        r'\{\{\$datetime\}\}': lambda: DataGenerator.datetime(),
        r'\{\{\$bool\}\}': lambda: DataGenerator.boolean(),
        r'\{\{\$int(\d+)?\}\}': lambda m: DataGenerator.integer(0, int(m.group(1)) if m and m.group(1) else 100),
        r'\{\{\$float\}\}': lambda: DataGenerator.float_num(),
    }
    
    @classmethod
    def render(cls, template: Union[str, Dict, List]) -> Any:
        """Render template with dynamic data"""
        if isinstance(template, dict):
            return {k: cls.render(v) for k, v in template.items()}
        elif isinstance(template, list):
            return [cls.render(item) for item in template]
        elif isinstance(template, str):
            return cls._render_string(template)
        return template
    
    @classmethod
    def _render_string(cls, template: str) -> str:
        """Render string template"""
        result = template
        
        # Handle repeat patterns: {{repeat(5)}}...{{/repeat}}
        repeat_pattern = r'\{\{repeat\((\d+)\)\}\}(.*?)\{\{/repeat\}\}'
        for match in re.finditer(repeat_pattern, result, re.DOTALL):
            count = int(match.group(1))
            content = match.group(2)
            repeated = [cls.render(json.loads(content)) for _ in range(count)]
            result = result.replace(match.group(0), json.dumps(repeated))
        
        # Handle simple patterns
        for pattern, generator in cls.PATTERNS.items():
            def replacer(match):
                try:
                    if callable(generator):
                        if hasattr(generator, '__code__') and generator.__code__.co_argcount > 0:
                            return str(generator(match))
                        return str(generator())
                    return str(generator)
                except:
                    return match.group(0)
            
            result = re.sub(pattern, replacer, result)
        
        return result

# Route Matcher
class RouteMatcher:
    """Match incoming requests to configured routes"""
    
    def __init__(self):
        self.routes: List[Dict] = []
    
    def add_route(self, method: str, path: str, response: Dict, 
                  query_params: Optional[Dict] = None,
                  headers: Optional[Dict] = None,
                  delay: int = 0):
        """Add a route configuration"""
        # Convert path to regex pattern
        pattern = self._path_to_regex(path)
        
        self.routes.append({
            'method': method.upper(),
            'path_pattern': re.compile(pattern),
            'path_template': path,
            'response': response,
            'query_params': query_params or {},
            'headers': headers or {},
            'delay': delay
        })
    
    def _path_to_regex(self, path: str) -> str:
        """Convert path template to regex pattern"""
        # Replace :param with capture group
        pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', path)
        # Replace * with wildcard
        pattern = pattern.replace('*', '.*')
        return f'^{pattern}$'
    
    def match(self, method: str, path: str, 
              query_params: Optional[Dict] = None) -> Optional[Dict]:
        """Match request to route"""
        query_params = query_params or {}
        
        for route in self.routes:
            if route['method'] != method.upper():
                continue
            
            match = route['path_pattern'].match(path)
            if match:
                # Check query params if specified
                if route['query_params']:
                    for key, value in route['query_params'].items():
                        if key not in query_params or query_params[key] != value:
                            break
                    else:
                        return {**route, 'path_params': match.groupdict()}
                else:
                    return {**route, 'path_params': match.groupdict()}
        
        return None

# Request/Response Logger
class RequestLogger:
    """Log and store request/response history"""
    
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self.entries: List[Dict] = []
        self._lock = threading.Lock()
    
    def log(self, request: Dict, response: Dict, duration_ms: float):
        """Log a request/response pair"""
        entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'method': request.get('method'),
            'path': request.get('path'),
            'query_params': request.get('query_params'),
            'headers': request.get('headers'),
            'body': request.get('body'),
            'response_status': response.get('status'),
            'response_body': response.get('body'),
            'duration_ms': duration_ms
        }
        
        with self._lock:
            self.entries.append(entry)
            if len(self.entries) > self.max_entries:
                self.entries.pop(0)
    
    def get_entries(self, limit: int = 100) -> List[Dict]:
        """Get recent log entries"""
        with self._lock:
            return self.entries[-limit:]
    
    def clear(self):
        """Clear all log entries"""
        with self._lock:
            self.entries.clear()
    
    def get_stats(self) -> Dict:
        """Get request statistics"""
        with self._lock:
            if not self.entries:
                return {'total': 0, 'avg_duration': 0, 'status_counts': {}}
            
            total = len(self.entries)
            avg_duration = sum(e['duration_ms'] for e in self.entries) / total
            status_counts = {}
            for e in self.entries:
                status = e['response_status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                'total': total,
                'avg_duration': round(avg_duration, 2),
                'status_counts': status_counts
            }

# HTTP Request Handler
class MockRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mock server"""
    
    # Class-level shared resources
    route_matcher: Optional[RouteMatcher] = None
    request_logger: Optional[RequestLogger] = None
    default_response: Optional[Dict] = None
    enable_cors: bool = True
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
    
    def _set_headers(self, status_code: int = 200, custom_headers: Optional[Dict] = None):
        """Set response headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        
        if self.enable_cors:
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
        if custom_headers:
            for key, value in custom_headers.items():
                self.send_header(key, value)
        
        self.end_headers()
    
    def _read_body(self) -> Optional[str]:
        """Read request body"""
        content_length = self.headers.get('Content-Length')
        if content_length:
            return self.rfile.read(int(content_length)).decode('utf-8')
        return None
    
    def _handle_request(self, method: str):
        """Handle incoming request"""
        start_time = time.time()
        
        # Parse URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        # Flatten single-value query params
        query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        
        # Read body
        body = self._read_body()
        
        # Build request object
        request = {
            'method': method,
            'path': path,
            'query_params': query_params,
            'headers': dict(self.headers),
            'body': body
        }
        
        # Match route
        route = None
        if self.route_matcher:
            route = self.route_matcher.match(method, path, query_params)
        
        # Build response
        if route:
            # Apply delay if specified
            if route.get('delay', 0) > 0:
                time.sleep(route['delay'] / 1000)
            
            response_config = route['response']
            status_code = response_config.get('status', 200)
            headers = response_config.get('headers', {})
            body_template = response_config.get('body', {})
            
            # Render template
            response_body = TemplateEngine.render(body_template)
        else:
            # Default 404 response
            if self.default_response:
                status_code = self.default_response.get('status', 404)
                headers = self.default_response.get('headers', {})
                response_body = self.default_response.get('body', {'error': 'Not Found'})
            else:
                status_code = 404
                headers = {}
                response_body = {'error': 'Not Found', 'path': path, 'method': method}
        
        # Send response
        self._set_headers(status_code, headers)
        response_json = json.dumps(response_body, ensure_ascii=False, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
        
        # Log request
        duration_ms = (time.time() - start_time) * 1000
        if self.request_logger:
            self.request_logger.log(request, {
                'status': status_code,
                'body': response_body
            }, duration_ms)
    
    def do_GET(self):
        self._handle_request('GET')
    
    def do_POST(self):
        self._handle_request('POST')
    
    def do_PUT(self):
        self._handle_request('PUT')
    
    def do_DELETE(self):
        self._handle_request('DELETE')
    
    def do_PATCH(self):
        self._handle_request('PATCH')
    
    def do_OPTIONS(self):
        self._set_headers(200)

# Mock Server
class MockServer:
    """Main mock server class"""
    
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.route_matcher = RouteMatcher()
        self.request_logger = RequestLogger()
        self.running = False
        self._thread: Optional[threading.Thread] = None
        
        # Set class-level resources
        MockRequestHandler.route_matcher = self.route_matcher
        MockRequestHandler.request_logger = self.request_logger
    
    def add_route(self, method: str, path: str, response: Dict, **kwargs):
        """Add a route"""
        self.route_matcher.add_route(method, path, response, **kwargs)
    
    def set_default_response(self, response: Dict):
        """Set default response for unmatched routes"""
        MockRequestHandler.default_response = response
    
    def enable_cors(self, enabled: bool = True):
        """Enable/disable CORS"""
        MockRequestHandler.enable_cors = enabled
    
    def start(self, blocking: bool = False):
        """Start the server"""
        self.server = HTTPServer((self.host, self.port), MockRequestHandler)
        self.running = True
        
        if blocking:
            self.server.serve_forever()
        else:
            self._thread = threading.Thread(target=self.server.serve_forever)
            self._thread.daemon = True
            self._thread.start()
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server:
            self.server.shutdown()
            self.server.server_close()
    
    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Get request logs"""
        return self.request_logger.get_entries(limit)
    
    def get_stats(self) -> Dict:
        """Get server statistics"""
        return self.request_logger.get_stats()
    
    def clear_logs(self):
        """Clear request logs"""
        self.request_logger.clear()
    
    def is_running(self) -> bool:
        """Check if server is running"""
        return self.running

# Configuration Loader
class ConfigLoader:
    """Load configuration from JSON file"""
    
    @staticmethod
    def load(filepath: str) -> Dict:
        """Load configuration from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def save(filepath: str, config: Dict):
        """Save configuration to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def apply_to_server(cls, server: MockServer, config: Dict):
        """Apply configuration to server"""
        # Set default response
        if 'defaultResponse' in config:
            server.set_default_response(config['defaultResponse'])
        
        # Enable CORS
        if 'cors' in config:
            server.enable_cors(config['cors'].get('enabled', True))
        
        # Add routes
        for route in config.get('routes', []):
            server.add_route(
                method=route['method'],
                path=route['path'],
                response=route['response'],
                query_params=route.get('queryParams'),
                headers=route.get('headers'),
                delay=route.get('delay', 0)
            )

# OpenAPI Parser
class OpenAPIParser:
    """Parse OpenAPI/Swagger spec and generate mock routes"""
    
    @classmethod
    def parse(cls, spec: Dict) -> List[Dict]:
        """Parse OpenAPI spec and return route configurations"""
        routes = []
        
        paths = spec.get('paths', {})
        for path, methods in paths.items():
            for method, operation in methods.items():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    route = cls._operation_to_route(method, path, operation)
                    routes.append(route)
        
        return routes
    
    @classmethod
    def _operation_to_route(cls, method: str, path: str, operation: Dict) -> Dict:
        """Convert OpenAPI operation to route config"""
        # Generate response from schema
        responses = operation.get('responses', {})
        success_response = responses.get('200', responses.get('201', {}))
        
        body = cls._schema_to_mock(success_response.get('schema', {}))
        
        return {
            'method': method.upper(),
            'path': path,
            'response': {
                'status': 200,
                'body': body
            }
        }
    
    @classmethod
    def _schema_to_mock(cls, schema: Dict) -> Any:
        """Convert JSON schema to mock data"""
        schema_type = schema.get('type', 'object')
        
        if schema_type == 'object':
            result = {}
            properties = schema.get('properties', {})
            for prop, prop_schema in properties.items():
                result[prop] = cls._schema_to_mock(prop_schema)
            return result
        
        elif schema_type == 'array':
            items = schema.get('items', {})
            return [cls._schema_to_mock(items) for _ in range(3)]
        
        elif schema_type == 'string':
            format_type = schema.get('format', '')
            if format_type == 'uuid':
                return '{{$uuid}}'
            elif format_type == 'email':
                return '{{$email}}'
            elif format_type == 'date':
                return '{{$date}}'
            elif format_type == 'date-time':
                return '{{$datetime}}'
            else:
                return '{{$word}}'
        
        elif schema_type == 'integer':
            return '{{$int}}'
        
        elif schema_type == 'number':
            return '{{$float}}'
        
        elif schema_type == 'boolean':
            return '{{$bool}}'
        
        return None

# TUI Dashboard
class TUIDashboard:
    """Terminal User Interface Dashboard"""
    
    def __init__(self, server: MockServer):
        self.server = server
        self.running = False
        self._thread: Optional[threading.Thread] = None
    
    def start(self):
        """Start TUI dashboard"""
        self.running = True
        self._thread = threading.Thread(target=self._render_loop)
        self._thread.daemon = True
        self._thread.start()
    
    def stop(self):
        """Stop TUI dashboard"""
        self.running = False
    
    def _render_loop(self):
        """Main render loop"""
        while self.running:
            self._clear_screen()
            self._render_header()
            self._render_stats()
            self._render_recent_requests()
            self._render_footer()
            
            time.sleep(1)
    
    def _clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def _render_header(self):
        """Render dashboard header"""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    🚀 MockPilot-CLI v1.0.0                   ║")
        print("║         Lightweight API Mock Server Intelligent Engine       ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        status = f"{Colors.GREEN}● RUNNING{Colors.END}" if self.server.is_running() else f"{Colors.RED}● STOPPED{Colors.END}"
        print(f"Server Status: {status} | Host: {self.server.host}:{self.server.port}")
        print()
    
    def _render_stats(self):
        """Render statistics panel"""
        stats = self.server.get_stats()
        
        print(f"{Colors.BOLD}📊 Statistics{Colors.END}")
        print(f"  Total Requests: {Colors.YELLOW}{stats['total']}{Colors.END}")
        print(f"  Avg Response Time: {Colors.YELLOW}{stats['avg_duration']}ms{Colors.END}")
        
        if stats['status_counts']:
            print(f"  Status Distribution:")
            for status, count in sorted(stats['status_counts'].items()):
                color = Colors.GREEN if status < 300 else (Colors.YELLOW if status < 400 else Colors.RED)
                print(f"    {color}{status}{Colors.END}: {count}")
        print()
    
    def _render_recent_requests(self):
        """Render recent requests"""
        logs = self.server.get_logs(10)
        
        print(f"{Colors.BOLD}📋 Recent Requests (Last 10){Colors.END}")
        print(f"{'Time':<12} {'Method':<8} {'Path':<30} {'Status':<8} {'Duration':<10}")
        print("-" * 70)
        
        for log in reversed(logs):
            time_str = log['timestamp'][11:19]
            method = log['method']
            path = log['path'][:28] + '..' if len(log['path']) > 30 else log['path']
            status = log['response_status']
            duration = f"{log['duration_ms']:.1f}ms"
            
            status_color = Colors.GREEN if status < 300 else (Colors.YELLOW if status < 400 else Colors.RED)
            method_color = Colors.CYAN if method == 'GET' else (Colors.YELLOW if method == 'POST' else Colors.MAGENTA)
            
            print(f"{time_str:<12} {method_color}{method:<8}{Colors.END} {path:<30} {status_color}{status:<8}{Colors.END} {duration:<10}")
        
        if not logs:
            print(f"{Colors.YELLOW}  No requests yet...{Colors.END}")
        
        print()
    
    def _render_footer(self):
        """Render dashboard footer"""
        print(f"{Colors.BLUE}Press Ctrl+C to stop the server{Colors.END}")

# CLI Interface
class CLI:
    """Command Line Interface"""
    
    def __init__(self):
        self.server: Optional[MockServer] = None
        self.dashboard: Optional[TUIDashboard] = None
    
    def run(self, args: List[str]):
        """Run CLI with arguments"""
        if len(args) < 2:
            self._show_help()
            return
        
        command = args[1]
        
        if command == 'start':
            self._cmd_start(args[2:])
        elif command == 'init':
            self._cmd_init()
        elif command == 'validate':
            self._cmd_validate(args[2:])
        elif command == 'openapi':
            self._cmd_openapi(args[2:])
        elif command == 'version':
            print(f"MockPilot-CLI v{__version__}")
        elif command == 'help':
            self._show_help()
        else:
            print(f"Unknown command: {command}")
            self._show_help()
    
    def _show_help(self):
        """Show help message"""
        help_text = f"""
{Colors.CYAN}{Colors.BOLD}MockPilot-CLI v{__version__}{Colors.END} - Lightweight API Mock Server

Usage: mockpilot <command> [options]

Commands:
  start [config.json]    Start mock server with optional config file
  init                   Create a sample configuration file
  validate <config>      Validate configuration file
  openapi <spec.json>    Generate routes from OpenAPI spec
  version                Show version
  help                   Show this help

Examples:
  mockpilot start                    # Start with default routes
  mockpilot start config.json        # Start with config file
  mockpilot init                     # Create sample config
  mockpilot validate config.json     # Validate config

For more information: https://github.com/gitstq/MockPilot-CLI
"""
        print(help_text)
    
    def _cmd_start(self, args: List[str]):
        """Start command"""
        config_file = args[0] if args else None
        
        # Create server
        self.server = MockServer(host='localhost', port=8080)
        
        # Load config if provided
        if config_file and os.path.exists(config_file):
            try:
                config = ConfigLoader.load(config_file)
                ConfigLoader.apply_to_server(self.server, config)
                print(f"{Colors.GREEN}✓ Loaded configuration from {config_file}{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}✗ Failed to load config: {e}{Colors.END}")
                return
        else:
            # Add default routes
            self._add_default_routes()
            print(f"{Colors.YELLOW}ℹ Using default routes (no config file provided){Colors.END}")
        
        # Start server
        self.server.start()
        print(f"{Colors.GREEN}✓ Server started at http://localhost:8080{Colors.END}")
        
        # Start dashboard
        self.dashboard = TUIDashboard(self.server)
        self.dashboard.start()
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Shutting down...{Colors.END}")
            self.dashboard.stop()
            self.server.stop()
            print(f"{Colors.GREEN}✓ Server stopped{Colors.END}")
    
    def _cmd_init(self):
        """Init command - create sample config"""
        sample_config = {
            "cors": {"enabled": True},
            "defaultResponse": {
                "status": 404,
                "body": {"error": "Not Found"}
            },
            "routes": [
                {
                    "method": "GET",
                    "path": "/api/users",
                    "response": {
                        "status": 200,
                        "body": {
                            "data": "{{repeat(5)}}",
                            "template": {
                                "id": "{{$uuid}}",
                                "name": "{{$name}}",
                                "email": "{{$email}}",
                                "createdAt": "{{$datetime}}"
                            }
                        }
                    }
                },
                {
                    "method": "GET",
                    "path": "/api/users/:id",
                    "response": {
                        "status": 200,
                        "body": {
                            "id": "{{$uuid}}",
                            "name": "{{$name}}",
                            "email": "{{$email}}",
                            "phone": "{{$phone}}",
                            "company": "{{$company}}",
                            "bio": "{{$lorem}}"
                        }
                    }
                },
                {
                    "method": "POST",
                    "path": "/api/users",
                    "response": {
                        "status": 201,
                        "body": {
                            "id": "{{$uuid}}",
                            "message": "User created successfully"
                        }
                    }
                },
                {
                    "method": "GET",
                    "path": "/api/products",
                    "response": {
                        "status": 200,
                        "body": {
                            "products": "{{repeat(3)}}",
                            "template": {
                                "id": "{{$int(1000)}}",
                                "name": "{{$word}}",
                                "price": "{{$float}}",
                                "inStock": "{{$bool}}"
                            }
                        }
                    }
                }
            ]
        }
        
        ConfigLoader.save('mockpilot.json', sample_config)
        print(f"{Colors.GREEN}✓ Created mockpilot.json{Colors.END}")
        print(f"{Colors.CYAN}Start server with: mockpilot start mockpilot.json{Colors.END}")
    
    def _cmd_validate(self, args: List[str]):
        """Validate command"""
        if not args:
            print(f"{Colors.RED}Please provide a config file{Colors.END}")
            return
        
        config_file = args[0]
        if not os.path.exists(config_file):
            print(f"{Colors.RED}Config file not found: {config_file}{Colors.END}")
            return
        
        try:
            config = ConfigLoader.load(config_file)
            # Basic validation
            if 'routes' in config:
                for i, route in enumerate(config['routes']):
                    if 'method' not in route:
                        raise ValueError(f"Route {i}: missing 'method'")
                    if 'path' not in route:
                        raise ValueError(f"Route {i}: missing 'path'")
                    if 'response' not in route:
                        raise ValueError(f"Route {i}: missing 'response'")
            
            print(f"{Colors.GREEN}✓ Configuration is valid{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}✗ Validation failed: {e}{Colors.END}")
    
    def _cmd_openapi(self, args: List[str]):
        """OpenAPI command"""
        if not args:
            print(f"{Colors.RED}Please provide an OpenAPI spec file{Colors.END}")
            return
        
        spec_file = args[0]
        if not os.path.exists(spec_file):
            print(f"{Colors.RED}Spec file not found: {spec_file}{Colors.END}")
            return
        
        try:
            spec = ConfigLoader.load(spec_file)
            routes = OpenAPIParser.parse(spec)
            
            config = {
                "cors": {"enabled": True},
                "routes": routes
            }
            
            output_file = 'mockpilot.json'
            ConfigLoader.save(output_file, config)
            print(f"{Colors.GREEN}✓ Generated {len(routes)} routes from OpenAPI spec{Colors.END}")
            print(f"{Colors.GREEN}✓ Saved to {output_file}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}✗ Failed to parse OpenAPI spec: {e}{Colors.END}")
    
    def _add_default_routes(self):
        """Add default routes for quick start"""
        # Health check
        self.server.add_route('GET', '/health', {
            'status': 200,
            'body': {'status': 'healthy', 'timestamp': '{{$datetime}}'}
        })
        
        # Users API
        self.server.add_route('GET', '/api/users', {
            'status': 200,
            'body': {
                'users': [
                    {'id': '{{$uuid}}', 'name': '{{$name}}', 'email': '{{$email}}'},
                    {'id': '{{$uuid}}', 'name': '{{$name}}', 'email': '{{$email}}'},
                    {'id': '{{$uuid}}', 'name': '{{$name}}', 'email': '{{$email}}'}
                ]
            }
        })
        
        self.server.add_route('GET', '/api/users/:id', {
            'status': 200,
            'body': {
                'id': '{{$uuid}}',
                'name': '{{$name}}',
                'email': '{{$email}}',
                'phone': '{{$phone}}',
                'company': '{{$company}}'
            }
        })
        
        self.server.add_route('POST', '/api/users', {
            'status': 201,
            'body': {'id': '{{$uuid}}', 'message': 'User created'}
        })
        
        # Products API
        self.server.add_route('GET', '/api/products', {
            'status': 200,
            'body': {
                'products': [
                    {'id': 1, 'name': 'Product A', 'price': '{{$float}}'},
                    {'id': 2, 'name': 'Product B', 'price': '{{$float}}'},
                    {'id': 3, 'name': 'Product C', 'price': '{{$float}}'}
                ]
            }
        })

# Main entry point
def main():
    """Main entry point"""
    cli = CLI()
    cli.run(sys.argv)

if __name__ == '__main__':
    main()
