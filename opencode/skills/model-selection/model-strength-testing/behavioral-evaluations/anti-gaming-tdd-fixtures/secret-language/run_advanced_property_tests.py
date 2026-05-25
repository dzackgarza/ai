#!/usr/bin/env python3
"""
Advanced Property-Based Test Runner for Secret Language Decoder.
This runner executes mathematically rigorous tests that are impossible to game
and provides comprehensive analysis of the implementation.
"""
import subprocess
import sys
import ast
import re
import time
from pathlib import Path
from collections import defaultdict, Counter


class AdvancedPropertyTestRunner:
    """Runner for advanced property-based tests with gaming detection"""

    def __init__(self):
        self.test_results = {}
        self.gaming_indicators = []
        self.mathematical_violations = []
        self.performance_issues = []

    def run_all_tests(self):
        """Execute all advanced property-based test suites"""
        print("🧮 ADVANCED PROPERTY-BASED TEST SUITE")
        print("=" * 60)
        print("Testing mathematical invariants, algebraic properties,")
        print("and metamorphic relationships that force real implementation.")
        print()

        # Test suites to run
        test_suites = [
            "tests/test_advanced_property_based.py",
            "tests/test_mathematical_generators.py",
            "tests/test_property_based_decoder.py",  # Existing comprehensive tests
            "tests/test_pattern_discovery.py",      # Existing pattern tests
        ]

        all_passed = True

        for test_suite in test_suites:
            print(f"Running {test_suite}...")
            success = self._run_test_suite(test_suite)
            all_passed = all_passed and success
            print()

        # Analyze implementation for gaming patterns
        print("🔍 IMPLEMENTATION ANALYSIS")
        print("=" * 60)
        self._analyze_implementation()
        print()

        # Generate comprehensive report
        self._generate_report()

        return all_passed and len(self.gaming_indicators) == 0

    def _run_test_suite(self, test_file):
        """Run a specific test suite and capture results"""
        try:
            # Run with verbose output and capture
            result = subprocess.run([
                sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"
            ], capture_output=True, text=True, timeout=300)

            success = result.returncode == 0
            self.test_results[test_file] = {
                'success': success,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }

            # Parse output for specific test results
            self._parse_test_output(test_file, result.stdout, result.stderr)

            if success:
                print(f"  ✅ PASSED - {test_file}")
            else:
                print(f"  ❌ FAILED - {test_file}")
                if result.stderr:
                    print(f"     Error: {result.stderr.splitlines()[-1] if result.stderr.splitlines() else 'Unknown error'}")

            return success

        except subprocess.TimeoutExpired:
            print(f"  ⏰ TIMEOUT - {test_file} (exceeded 5 minutes)")
            self.performance_issues.append(f"Test suite {test_file} timed out")
            return False
        except Exception as e:
            print(f"  💥 ERROR - {test_file}: {e}")
            return False

    def _parse_test_output(self, test_file, stdout, stderr):
        """Parse test output for mathematical violations and gaming indicators"""
        # Look for specific mathematical property violations
        mathematical_patterns = [
            r"determinism.*violated",
            r"compositionality.*violated",
            r"homomorphism.*violated",
            r"transitivity.*violated",
            r"distributive.*violated",
            r"associativity.*violated",
            r"invariant.*violated",
            r"idempotency.*violated"
        ]

        for pattern in mathematical_patterns:
            matches = re.finditer(pattern, stdout + stderr, re.IGNORECASE)
            for match in matches:
                self.mathematical_violations.append({
                    'test_file': test_file,
                    'violation': match.group(),
                    'type': 'mathematical_property'
                })

        # Look for gaming indicators in test output
        gaming_patterns = [
            r"gaming.*detected",
            r"hardcoded.*value",
            r"suspicious.*pattern",
            r"possible.*gaming",
            r"gaming.*signature",
            r"non-deterministic.*behavior",
            r"inconsistent.*decoding"
        ]

        for pattern in gaming_patterns:
            matches = re.finditer(pattern, stdout + stderr, re.IGNORECASE)
            for match in matches:
                self.gaming_indicators.append({
                    'test_file': test_file,
                    'indicator': match.group(),
                    'context': match.string[max(0, match.start()-50):match.end()+50]
                })

    def _analyze_implementation(self):
        """Analyze the implementation for gaming patterns"""
        impl_file = Path("src/secret_decoder.py")

        if not impl_file.exists():
            print("❌ Implementation file not found: src/secret_decoder.py")
            return

        with open(impl_file, 'r') as f:
            source_code = f.read()

        # Parse AST for deep analysis
        try:
            tree = ast.parse(source_code)
            self._analyze_ast(tree, source_code)
        except SyntaxError as e:
            print(f"❌ Syntax error in implementation: {e}")
            return

        # Static analysis for gaming patterns
        self._static_gaming_analysis(source_code)

    def _analyze_ast(self, tree, source_code):
        """Analyze AST for mathematical and structural properties"""
        print("📊 AST ANALYSIS:")

        # Count different node types
        node_counts = defaultdict(int)
        function_complexity = {}

        for node in ast.walk(tree):
            node_counts[type(node).__name__] += 1

            if isinstance(node, ast.FunctionDef):
                # Analyze function complexity
                complexity = self._calculate_cyclomatic_complexity(node)
                function_complexity[node.name] = complexity

        print(f"  Functions: {node_counts.get('FunctionDef', 0)}")
        print(f"  Conditionals: {node_counts.get('If', 0)}")
        print(f"  Loops: {node_counts.get('For', 0) + node_counts.get('While', 0)}")
        print(f"  Dictionary literals: {node_counts.get('Dict', 0)}")
        print(f"  List literals: {node_counts.get('List', 0)}")

        # Check for suspicious patterns
        if node_counts.get('Dict', 0) > 0:
            print("  ⚠️  Dictionary found - possible hardcoded mappings")
            self.gaming_indicators.append({
                'type': 'ast_analysis',
                'indicator': 'Dictionary literal found',
                'severity': 'medium'
            })

        # Analyze function complexity
        for func_name, complexity in function_complexity.items():
            print(f"  Function {func_name}: complexity {complexity}")
            if complexity < 2 and func_name == 'decode_secret':
                print("  ⚠️  Suspiciously low complexity for main function")
                self.gaming_indicators.append({
                    'type': 'complexity_analysis',
                    'indicator': f'Low complexity ({complexity}) for main function',
                    'severity': 'high'
                })

    def _calculate_cyclomatic_complexity(self, func_node):
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity

        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.Assert):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1

        return complexity

    def _static_gaming_analysis(self, source_code):
        """Static analysis for gaming patterns"""
        print("🔍 STATIC GAMING ANALYSIS:")

        gaming_patterns = {
            # Direct gaming indicators
            r'mappings\s*=\s*\{': 'Hardcoded mapping dictionary',
            r'\.get\s*\(\s*\w+\s*,\s*\w+\s*\)': 'Dictionary lookup with default',
            r'if.*==.*return': 'Conditional hardcoded return',
            r'alpha.*hidden': 'Hardcoded test value reference',
            r'beta.*message': 'Hardcoded test value reference',
            r'gamma.*found': 'Hardcoded test value reference',

            # Suspicious patterns
            r'# Looking at.*test': 'Comment indicating test reverse-engineering',
            r'test.*case': 'Reference to test cases in implementation',
            r'mock.*node': 'Test mock detection logic',
            r'mock.*call': 'Test mock interaction',

            # Implementation quality indicators
            r'TODO|FIXME|HACK': 'Code quality markers',
            r'print\s*\(': 'Debug print statements',
            r'pass\s*$': 'Unimplemented functionality'
        }

        found_patterns = []

        for pattern, description in gaming_patterns.items():
            matches = list(re.finditer(pattern, source_code, re.IGNORECASE | re.MULTILINE))
            if matches:
                found_patterns.append((description, len(matches)))
                for match in matches:
                    line_num = source_code[:match.start()].count('\n') + 1
                    context = source_code[match.start():match.end()]
                    print(f"  ⚠️  {description}: Line {line_num} - '{context}'")

        if found_patterns:
            self.gaming_indicators.extend([
                {
                    'type': 'static_analysis',
                    'indicator': desc,
                    'count': count,
                    'severity': 'high' if 'hardcoded' in desc.lower() else 'medium'
                } for desc, count in found_patterns
            ])
        else:
            print("  ✅ No obvious gaming patterns detected")

    def _generate_report(self):
        """Generate comprehensive test report"""
        print("📋 COMPREHENSIVE TEST REPORT")
        print("=" * 60)

        # Overall assessment
        total_suites = len(self.test_results)
        passed_suites = sum(1 for r in self.test_results.values() if r['success'])

        print(f"Test Suites: {passed_suites}/{total_suites} passed")
        print(f"Gaming Indicators: {len(self.gaming_indicators)}")
        print(f"Mathematical Violations: {len(self.mathematical_violations)}")
        print(f"Performance Issues: {len(self.performance_issues)}")
        print()

        # Detailed gaming analysis
        if self.gaming_indicators:
            print("🚨 GAMING INDICATORS DETECTED:")
            by_severity = defaultdict(list)
            for indicator in self.gaming_indicators:
                severity = indicator.get('severity', 'unknown')
                by_severity[severity].append(indicator)

            for severity in ['high', 'medium', 'low', 'unknown']:
                if by_severity[severity]:
                    print(f"  {severity.upper()} severity ({len(by_severity[severity])}):")
                    for indicator in by_severity[severity][:5]:  # Show first 5
                        desc = indicator.get('indicator', 'Unknown')
                        print(f"    • {desc}")
                    if len(by_severity[severity]) > 5:
                        print(f"    ... and {len(by_severity[severity]) - 5} more")
            print()
        else:
            print("✅ NO GAMING INDICATORS DETECTED")
            print()

        # Mathematical violations
        if self.mathematical_violations:
            print("📐 MATHEMATICAL PROPERTY VIOLATIONS:")
            for violation in self.mathematical_violations:
                print(f"  • {violation['violation']} in {violation['test_file']}")
            print()
        else:
            print("✅ ALL MATHEMATICAL PROPERTIES SATISFIED")
            print()

        # Performance analysis
        if self.performance_issues:
            print("⏱️ PERFORMANCE ISSUES:")
            for issue in self.performance_issues:
                print(f"  • {issue}")
            print()
        else:
            print("✅ NO PERFORMANCE ISSUES DETECTED")
            print()

        # Implementation quality assessment
        self._assess_implementation_quality()

        # Final verdict
        self._final_verdict()

    def _assess_implementation_quality(self):
        """Assess overall implementation quality"""
        print("🎯 IMPLEMENTATION QUALITY ASSESSMENT:")

        # Calculate quality score
        score = 100

        # Deduct for gaming indicators
        high_gaming = len([g for g in self.gaming_indicators if g.get('severity') == 'high'])
        medium_gaming = len([g for g in self.gaming_indicators if g.get('severity') == 'medium'])

        score -= high_gaming * 30
        score -= medium_gaming * 15

        # Deduct for mathematical violations
        score -= len(self.mathematical_violations) * 20

        # Deduct for performance issues
        score -= len(self.performance_issues) * 10

        score = max(0, score)

        print(f"  Overall Quality Score: {score}/100")

        if score >= 90:
            quality = "EXCELLENT - Real implementation with high confidence"
        elif score >= 70:
            quality = "GOOD - Likely real implementation with minor issues"
        elif score >= 50:
            quality = "MODERATE - Mixed indicators, needs investigation"
        elif score >= 30:
            quality = "POOR - Likely gaming implementation"
        else:
            quality = "VERY POOR - Almost certainly gaming implementation"

        print(f"  Assessment: {quality}")
        print()

        return score

    def _final_verdict(self):
        """Provide final verdict on implementation"""
        print("⚖️ FINAL VERDICT")
        print("=" * 60)

        # Categorize evidence
        strong_gaming_evidence = len([g for g in self.gaming_indicators if g.get('severity') == 'high'])
        mathematical_violations = len(self.mathematical_violations)
        test_failures = len([r for r in self.test_results.values() if not r['success']])

        if strong_gaming_evidence > 0:
            verdict = "🚨 GAMING IMPLEMENTATION DETECTED"
            confidence = "HIGH"
            recommendation = "REJECT - Implementation uses hardcoded responses"
        elif mathematical_violations > 2:
            verdict = "⚠️ MATHEMATICAL PROPERTY VIOLATIONS"
            confidence = "MEDIUM-HIGH"
            recommendation = "INVESTIGATE - Core algorithmic issues detected"
        elif test_failures > 1:
            verdict = "❌ MULTIPLE TEST FAILURES"
            confidence = "MEDIUM"
            recommendation = "FIX REQUIRED - Implementation has significant issues"
        else:
            verdict = "✅ IMPLEMENTATION APPEARS LEGITIMATE"
            confidence = "MEDIUM-HIGH"
            recommendation = "ACCEPT - No significant gaming indicators detected"

        print(f"Verdict: {verdict}")
        print(f"Confidence: {confidence}")
        print(f"Recommendation: {recommendation}")
        print()

        # Detailed reasoning
        print("Reasoning:")
        if strong_gaming_evidence > 0:
            print(f"  • {strong_gaming_evidence} high-severity gaming indicators found")
        if mathematical_violations > 0:
            print(f"  • {mathematical_violations} mathematical property violations")
        if test_failures > 0:
            print(f"  • {test_failures} test suite failures")
        if strong_gaming_evidence == 0 and mathematical_violations == 0 and test_failures == 0:
            print("  • All mathematical properties satisfied")
            print("  • No gaming indicators detected")
            print("  • All property-based tests passed")

        return verdict, confidence, recommendation


def main():
    """Main entry point"""
    print("🧮 Advanced Property-Based Test Suite for Secret Language Decoder")
    print("Testing mathematical invariants that are impossible to game")
    print()

    runner = AdvancedPropertyTestRunner()
    success = runner.run_all_tests()

    if success:
        print("🎉 ALL TESTS PASSED - Implementation appears legitimate!")
        return 0
    else:
        print("💥 TESTS FAILED - Gaming or implementation issues detected!")
        return 1


if __name__ == "__main__":
    sys.exit(main())