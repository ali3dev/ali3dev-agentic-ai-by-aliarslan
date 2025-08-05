"""
Multi-Agent System Testing Suite
Comprehensive testing of all agents, tools, and coordination
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_system import MultiAgentSystem
import time
import json

class TestRunner:
    def __init__(self):
        self.system = MultiAgentSystem()
        self.test_results = []
        
    def run_test(self, test_name, test_function):
        """Run a single test and record results"""
        print(f"\nRunning: {test_name}")
        print("-" * 50)
        
        start_time = time.time()
        try:
            result = test_function()
            end_time = time.time()
            
            test_result = {
                'name': test_name,
                'status': 'PASSED' if result else 'FAILED',
                'duration': f"{end_time - start_time:.2f}s",
                'success': result
            }
            
            self.test_results.append(test_result)
            
            status_icon = "PASSED" if result else "FAILED"
            print(f"{status_icon} {test_name}: {test_result['status']} ({test_result['duration']})")
            
            return result
            
        except Exception as e:
            end_time = time.time()
            
            test_result = {
                'name': test_name,
                'status': 'ERROR',
                'duration': f"{end_time - start_time:.2f}s",
                'error': str(e),
                'success': False
            }
            
            self.test_results.append(test_result)
            print(f"ERROR {test_name}: ERROR - {str(e)}")
            
            return False

def test_individual_agents():
    """Test each agent individually"""
    runner = TestRunner()
    
    def test_manager_agent():
        plan, project_id = runner.system.manager.delegate_task("Create a test document")
        return project_id is not None and "GOAL" in plan
    
    def test_researcher_agent():
        result = runner.system.researcher.conduct_research("artificial intelligence", "general")
        return len(result) > 100 and "research" in result.lower()
    
    def test_writer_agent():
        result = runner.system.writer.create_content("article", "test topic", "professional")
        return len(result) > 100 and "test topic" in result.lower()
    
    def test_critic_agent():
        test_content = "This is a test article. It has multiple sentences. The quality should be assessed."
        result = runner.system.critic.review_content(test_content, "article")
        return "GOAL" in result and "quality" in result.lower()
    
    def test_analyst_agent():
        data = [1, 2, 3, 4, 5]
        result = runner.system.analyst.analyze_data(data, "trend_analysis", "Identify trends in the data")
        return result is not None and ("GOAL" in result or "insight" in result.lower())
    
    # Run individual agent tests
    tests = [
        ("Manager Agent Delegation", test_manager_agent),
        ("Researcher Agent Research", test_researcher_agent),
        ("Writer Agent Content Creation", test_writer_agent),
        ("Critic Agent Quality Review", test_critic_agent),
        ("Analyst Agent Data Analysis", test_analyst_agent)
    ]
    
    results = []
    for test_name, test_func in tests:
        results.append(runner.run_test(test_name, test_func))
    
    return all(results)

def test_agent_coordination():
    """Test multi-agent coordination"""
    runner = TestRunner()
    
    coordination_tests = [
        "Create a short blog post about technology",
        "Research market trends and provide analysis",
        "Write a business summary with recommendations"
    ]
    
    def test_coordination():
        success_count = 0
        for request in coordination_tests:
            try:
                runner.system.start_session(f"coord_test_{coordination_tests.index(request)}")
                response = runner.system.process_request(request)
                
                # Check if response contains agentic pattern
                if "GOAL" in response and len(response) > 200:
                    success_count += 1
                    print(f"   PASSED Coordination test: {request[:30]}...")
                else:
                    print(f"   FAILED Coordination test: {request[:30]}...")
                    
            except Exception as e:
                print(f"   ERROR Coordination: {str(e)}")
        
        return success_count >= len(coordination_tests) * 0.8  # 80% success rate

    return runner.run_test("Multi-Agent Coordination", test_coordination)

def test_tools_integration():
    """Test advanced tools integration"""
    runner = TestRunner()
    
    def test_web_search_tool():
        results = runner.system.web_search.search("artificial intelligence", max_results=3)
        return len(results) >= 3 and all(hasattr(r, 'title') for r in results)
    
    def test_content_tools():
        test_content = "# Test Heading\n\nThis is a test paragraph with **bold** text."
        structure = runner.system.content_processor.extract_structure(test_content)
        return structure['word_count'] > 0 and len(structure['headings']) > 0
    
    def test_analysis_tools():
        test_data = [10, 20, 15, 25, 30, 18, 22]
        analysis = runner.system.data_analyzer.statistical_analysis(test_data)
        return 'mean' in analysis and 'median' in analysis
    
    def test_quality_validation():
        test_content = "This is a test content for quality validation."
        validation = runner.system.content_validator.validate_quality(test_content)
        return 'overall_score' in validation and validation['overall_score'] > 0
    
    # Run tool tests
    tool_tests = [
        ("Web Search Tool", test_web_search_tool),
        ("Content Processing Tools", test_content_tools),
        ("Data Analysis Tools", test_analysis_tools),
        ("Quality Validation Tools", test_quality_validation)
    ]
    
    results = []
    for test_name, test_func in tool_tests:
        results.append(runner.run_test(test_name, test_func))
    
    return all(results)

def test_memory_systems():
    """Test memory and communication systems"""
    runner = TestRunner()
    
    def test_shared_memory():
        # Test fact storage and retrieval
        runner.system.shared_memory.store_fact("test", "key1", "value1", "test_agent")
        retrieved = runner.system.shared_memory.get_fact("test", "key1", "test_agent")
        
        # Test insight storage
        runner.system.shared_memory.store_insight("test_topic", "test insight", "test_agent")
        insights = runner.system.shared_memory.get_insights("test_topic", "test_agent")
        
        return retrieved is not None and len(insights) > 0
    
    def test_conversation_history():
        session_id = runner.system.conversation_history.start_session("test_user")
        runner.system.conversation_history.add_message(session_id, "user", "test message")
        context = runner.system.conversation_history.get_session_context(session_id)
        
        return len(context['recent_messages']) > 0
    
    def test_message_hub():
        msg_id = runner.system.message_hub.send_message("agent1", "agent2", "test", "test message")
        messages = runner.system.message_hub.get_messages_for_agent("agent2")
        
        return len(messages) > 0
    
    # Run memory system tests
    memory_tests = [
        ("Shared Memory System", test_shared_memory),
        ("Conversation History", test_conversation_history),
        ("Message Hub Communication", test_message_hub)
    ]
    
    results = []
    for test_name, test_func in memory_tests:
        results.append(runner.run_test(test_name, test_func))
    
    return all(results)

def test_error_handling():
    """Test system error handling and resilience"""
    runner = TestRunner()
    
    def test_invalid_requests():
        error_cases = [
            "",  # Empty request
            "x" * 10000,  # Very long request
            "Invalid request with special chars: @#$%^&*()",
            None  # None input
        ]
        
        handled_gracefully = 0
        for case in error_cases:
            try:
                if case is None:
                    continue
                runner.system.start_session("error_test")
                response = runner.system.process_request(case)
                
                # Check if error was handled gracefully
                if "error" in response.lower() or len(response) > 0:
                    handled_gracefully += 1
                    
            except Exception:
                # Even exceptions should be handled gracefully in production
                pass
        
        return handled_gracefully >= len([c for c in error_cases if c is not None]) * 0.8
    
    def test_agent_failure_recovery():
        # This would test what happens if an agent fails
        # For now, we'll test basic resilience
        try:
            runner.system.start_session("recovery_test")
            response = runner.system.process_request("Simple test request")
            return len(response) > 0
        except:
            return False
    
    # Run error handling tests
    error_tests = [
        ("Invalid Request Handling", test_invalid_requests),
        ("Agent Failure Recovery", test_agent_failure_recovery)
    ]
    
    results = []
    for test_name, test_func in error_tests:
        results.append(runner.run_test(test_name, test_func))
    
    return all(results)

def test_performance_benchmarks():
    """Test system performance benchmarks"""
    runner = TestRunner()
    
    def test_response_time():
        test_requests = [
            "What is AI?",
            "Create a short summary",
            "Analyze basic data"
        ]
        
        total_time = 0
        successful_requests = 0
        
        for request in test_requests:
            start_time = time.time()
            try:
                runner.system.start_session(f"perf_test_{test_requests.index(request)}")
                response = runner.system.process_request(request)
                end_time = time.time()
                
                processing_time = end_time - start_time
                total_time += processing_time
                
                if len(response) > 50:  # Meaningful response
                    successful_requests += 1
                    
            except Exception:
                pass
        
        if successful_requests > 0:
            avg_time = total_time / successful_requests
            print(f"   Average response time: {avg_time:.2f} seconds")
            print(f"   Success rate: {successful_requests}/{len(test_requests)}")
            
            # Performance targets: <30 seconds average, >80% success rate
            return avg_time < 30 and (successful_requests / len(test_requests)) > 0.8
        
        return False
    
    def test_memory_usage():
        # Basic memory usage test
        initial_memory = len(str(runner.system.shared_memory.knowledge_base))
        
        # Add some data
        for i in range(10):
            runner.system.shared_memory.store_fact(f"test_cat_{i}", f"key_{i}", f"value_{i}", "test")
        
        final_memory = len(str(runner.system.shared_memory.knowledge_base))
        
        # Memory should have increased
        return final_memory > initial_memory
    
    # Run performance tests
    performance_tests = [
        ("Response Time Performance", test_response_time),
        ("Memory Usage Test", test_memory_usage)
    ]
    
    results = []
    for test_name, test_func in performance_tests:
        results.append(runner.run_test(test_name, test_func))
    
    return all(results)

def run_comprehensive_test_suite():
    """Run all tests and generate comprehensive report"""
    print("Multi-Agent System - Comprehensive Test Suite")
    print("="*80)
    
    test_suites = [
        ("Individual Agents", test_individual_agents),
        ("Agent Coordination", test_agent_coordination),
        ("Tools Integration", test_tools_integration),
        ("Memory Systems", test_memory_systems),
        ("Error Handling", test_error_handling),
        ("Performance Benchmarks", test_performance_benchmarks)
    ]

    suite_results = []
    total_start_time = time.time()
    
    for suite_name, suite_function in test_suites:
        print(f"\n{'='*20} {suite_name} {'='*20}")
        
        suite_start_time = time.time()
        try:
            result = suite_function()
            suite_end_time = time.time()
            
            suite_results.append({
                'name': suite_name,
                'success': result,
                'duration': f"{suite_end_time - suite_start_time:.2f}s"
            })
            
            status = "PASSED" if result else "FAILED"
            print(f"\n{status} {suite_name} completed in {suite_end_time - suite_start_time:.2f}s")
            
        except Exception as e:
            suite_end_time = time.time()
            suite_results.append({
                'name': suite_name,
                'success': False,
                'duration': f"{suite_end_time - suite_start_time:.2f}s",
                'error': str(e)
            })
            print(f"\nFAILED {suite_name} with error: {str(e)}")
    
    total_end_time = time.time()

# Generate comprehensive report
    print(f"\n{'='*80}")
    print("COMPREHENSIVE TEST REPORT")
    print("="*80)
    
    passed_suites = sum(1 for result in suite_results if result['success'])
    total_suites = len(suite_results)
    
    print(f"Overall Results: {passed_suites}/{total_suites} test suites passed")
    print(f"Total execution time: {total_end_time - total_start_time:.2f} seconds")
    print(f"Success rate: {(passed_suites/total_suites)*100:.1f}%")
    
    print(f"\nDetailed Results:")
    for result in suite_results:
        status_icon = "PASSED" if result['success'] else "FAILED"
        print(f"   {status_icon} {result['name']:<25} {result['duration']:>8}")
        if not result['success'] and 'error' in result:
            print(f"      Error: {result['error']}")
    
    # System health assessment
    print(f"\nSystem Health Assessment:")
    if passed_suites == total_suites:
        print("    EXCELLENT: All systems operational and performing optimally")
        print("    Ready for production deployment")
    elif passed_suites >= total_suites * 0.8:
        print("    GOOD: System mostly functional with minor issues")
        print("    Address failed tests before production")
    elif passed_suites >= total_suites * 0.6:
        print("    FAIR: System partially functional, significant issues present")
        print("    Major fixes required before deployment")
    else:
        print("    POOR: System has critical issues")
        print("    Extensive debugging and fixes required")
    
    # Recommendations
    failed_suites = [r for r in suite_results if not r['success']]
    if failed_suites:
        print(f"\nRecommendations:")
        for failed_suite in failed_suites:
            suite_name = failed_suite['name']
            if 'Individual Agents' in suite_name:
                print("   • Check agent implementations and API connectivity")
            elif 'Coordination' in suite_name:
                print("   • Review inter-agent communication protocols")
            elif 'Tools' in suite_name:
                print("   • Verify tool integrations and dependencies")
            elif 'Memory' in suite_name:
                print("   • Check memory system configurations")
            elif 'Error Handling' in suite_name:
                print("   • Improve error handling and resilience mechanisms")
            elif 'Performance' in suite_name:
                print("   • Optimize system performance and resource usage")
    
    print("="*80)
    
    return passed_suites == total_suites

def main():
    """Main test execution"""
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "agents":
            test_individual_agents()
        elif test_type == "coordination":
            test_agent_coordination()
        elif test_type == "tools":
            test_tools_integration()
        elif test_type == "memory":
            test_memory_systems()
        elif test_type == "errors":
            test_error_handling()
        elif test_type == "performance":
            test_performance_benchmarks()
        elif test_type == "quick":
            # Quick test mode
            print("Quick Test Mode")
            print("="*50)
            
            system = MultiAgentSystem()
            system.start_session("quick_test")
            
            test_request = "Create a short test response"
            print(f"Testing request: {test_request}")
            
            response = system.process_request(test_request)
            
            if len(response) > 50 and "GOAL" in response:
                print("PASSED Quick test - System is working!")
            else:
                print("FAILED Quick test - Check system configuration")
        
        else:
            print("Available test types:")
            print("  agents      - Test individual agents")
            print("  coordination - Test multi-agent coordination")
            print("  tools       - Test tools integration")
            print("  memory      - Test memory systems")
            print("  errors      - Test error handling")
            print("  performance - Test performance benchmarks")
            print("  quick       - Quick functionality test")
            print("  all         - Run comprehensive test suite")
    else:
        run_comprehensive_test_suite()

if __name__ == "__main__":
    main()

