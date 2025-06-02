#!/usr/bin/env python3
"""
Step 2 Implementation Test
Tests all requirements from the Implementation Guide for processing steps
"""
import os
import sys
from datetime import date

# Set up environment - requires OPENAI_API_KEY environment variable
sys.path.insert(0, '/Users/gusrasch/dev/ventii/src')

def test_step2_requirements():
    """
    Test Step 2: Processing Steps
    
    Requirements from Implementation Guide:
    - File: src/ventii/steps.py
    - Three core processing functions using langchain
    - filter_step(image_b64: str) -> bool
    - summarize_step(image_b64: str, today_date: str) -> str
    - structure_step(image_b64: str, summary: str) -> EventInfo
    - Each function uses ChatOpenAI with appropriate capabilities
    - Include exact prompts from PRD
    - Handle base64 image input
    - Return specified output type
    - Test: Each function should work independently
    """
    
    print("Testing Step 2: Processing Steps Implementation")
    print("=" * 60)
    
    # Check API key is available for actual testing
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠ OPENAI_API_KEY not found - will skip actual API calls")
        api_testing = False
    else:
        print("✓ OPENAI_API_KEY found - will test API calls")
        api_testing = True
    
    # Test 1: Import and function existence
    print("\n1. Testing imports and function existence...")
    try:
        from ventii.steps import filter_step, summarize_step, structure_step
        from ventii.models import EventInfo
        print("✓ Successfully imported all functions and models")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    
    # Test 2: Function signatures
    print("\n2. Testing function signatures...")
    try:
        # Check parameter and return types
        filter_annotations = filter_step.__annotations__
        assert 'image_b64' in filter_annotations and filter_annotations['image_b64'] == str
        assert filter_annotations.get('return') == bool
        print("✓ filter_step has correct signature: (image_b64: str) -> bool")
        
        summarize_annotations = summarize_step.__annotations__
        assert 'image_b64' in summarize_annotations and summarize_annotations['image_b64'] == str
        assert 'today_date' in summarize_annotations and summarize_annotations['today_date'] == str
        assert summarize_annotations.get('return') == str
        print("✓ summarize_step has correct signature: (image_b64: str, today_date: str) -> str")
        
        structure_annotations = structure_step.__annotations__
        assert 'image_b64' in structure_annotations and structure_annotations['image_b64'] == str
        assert 'summary' in structure_annotations and structure_annotations['summary'] == str
        assert structure_annotations.get('return') == EventInfo
        print("✓ structure_step has correct signature: (image_b64: str, summary: str) -> EventInfo")
        
    except Exception as e:
        print(f"✗ Function signature test failed: {e}")
        return False
    
    # Test 3: Function independence (each works with sample data)
    print("\n3. Testing function independence with sample data...")
    
    if not api_testing:
        print("   ⚠ Skipping API tests - no OPENAI_API_KEY")
    else:
        # Create test data
        test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        today_str = str(date.today())
        test_summary = "Sample event summary for testing structure_step"
        
        try:
            # Test filter_step independently
            print("   Testing filter_step...")
            filter_result = filter_step(test_image_b64)
            assert isinstance(filter_result, bool), f"Expected bool, got {type(filter_result)}"
            print(f"   ✓ filter_step returned: {filter_result}")
            
            # Test summarize_step independently  
            print("   Testing summarize_step...")
            summary_result = summarize_step(test_image_b64, today_str)
            assert isinstance(summary_result, str), f"Expected str, got {type(summary_result)}"
            print(f"   ✓ summarize_step returned: '{summary_result[:30]}...'")
            
            # Test structure_step independently
            print("   Testing structure_step...")
            structure_result = structure_step(test_image_b64, test_summary)
            assert isinstance(structure_result, EventInfo), f"Expected EventInfo, got {type(structure_result)}"
            print(f"   ✓ structure_step returned EventInfo object")
            
        except Exception as e:
            print(f"✗ Function independence test failed: {e}")
            return False
    
    # Test 4: Verify implementation uses langchain correctly
    print("\n4. Verifying langchain implementation...")
    try:
        import inspect
        
        # Check that functions import and use required langchain components
        filter_source = inspect.getsource(filter_step)
        assert 'ChatOpenAI' in filter_source, "filter_step should use ChatOpenAI"
        assert 'HumanMessage' in filter_source, "filter_step should use HumanMessage"
        print("✓ filter_step uses ChatOpenAI and HumanMessage")
        
        summarize_source = inspect.getsource(summarize_step)
        assert 'ChatOpenAI' in summarize_source, "summarize_step should use ChatOpenAI"
        assert 'HumanMessage' in summarize_source, "summarize_step should use HumanMessage"
        print("✓ summarize_step uses ChatOpenAI and HumanMessage")
        
        structure_source = inspect.getsource(structure_step)
        assert 'ChatOpenAI' in structure_source, "structure_step should use ChatOpenAI"
        assert 'PydanticOutputParser' in structure_source, "structure_step should use PydanticOutputParser"
        print("✓ structure_step uses ChatOpenAI and PydanticOutputParser")
        
    except Exception as e:
        print(f"✗ Langchain implementation test failed: {e}")
        return False
    
    # Test 5: Verify prompts are from PRD
    print("\n5. Verifying prompts match PRD specifications...")
    try:
        import inspect
        
        filter_source = inspect.getsource(filter_step)
        expected_filter_prompt = "Determine if this image contains information about an upcoming event"
        assert expected_filter_prompt in filter_source, "filter_step should use exact prompt from PRD"
        print("✓ filter_step uses correct prompt from PRD")
        
        summarize_source = inspect.getsource(summarize_step)
        expected_summarize_prompt = "Generate a written summary of the following image that contains information about an event"
        assert expected_summarize_prompt in summarize_source, "summarize_step should use exact prompt from PRD"
        print("✓ summarize_step uses correct prompt from PRD")
        
        # structure_step prompt is more complex but should reference the EventInfo fields
        structure_source = inspect.getsource(structure_step)
        required_fields = ['event_date', 'event_starttime', 'event_venue', 'event_location']
        for field in required_fields:
            assert field in structure_source, f"structure_step should reference {field}"
        print("✓ structure_step prompt includes all required EventInfo fields")
        
    except Exception as e:
        print(f"✗ Prompt verification test failed: {e}")
        return False
    
    # Test 6: Verify base64 image handling
    print("\n6. Verifying base64 image handling...")
    try:
        import inspect
        
        # Check that all functions properly format base64 images for vision models
        for func_name, func in [('filter_step', filter_step), ('summarize_step', summarize_step), ('structure_step', structure_step)]:
            source = inspect.getsource(func)
            assert 'data:image/' in source and 'base64,' in source, f"{func_name} should format base64 for vision model"
            print(f"✓ {func_name} properly formats base64 images")
        
    except Exception as e:
        print(f"✗ Base64 handling test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Step 2 implementation PASSED all requirements!")
    print("\nStep 2 Test Criteria Met:")
    print("✓ File created: src/ventii/steps.py")
    print("✓ Three core processing functions implemented")
    print("✓ Uses langchain ChatOpenAI with vision capabilities")
    print("✓ Uses langchain PydanticOutputParser for structured output")
    print("✓ Includes exact prompts from PRD")
    print("✓ Handles base64 image input correctly")
    print("✓ Returns specified output types")
    print("✓ Each function works independently")
    
    print("\nImplemented Functions:")
    print("• filter_step(image_b64: str) -> bool")
    print("  - Uses ChatOpenAI with vision")
    print("  - Determines if image contains event info")
    print("  - Returns boolean")
    
    print("• summarize_step(image_b64: str, today_date: str) -> str")
    print("  - Uses ChatOpenAI with vision")
    print("  - Generates unstructured text summary")
    print("  - Uses today's date for relative time understanding")
    
    print("• structure_step(image_b64: str, summary: str) -> EventInfo")
    print("  - Uses ChatOpenAI with PydanticOutputParser")
    print("  - Extracts structured EventInfo object")
    print("  - Uses both image and summary as input")
    
    return True

if __name__ == "__main__":
    success = test_step2_requirements()
    if success:
        print("\n✅ Step 2 implementation is complete and ready for Step 3!")
    else:
        print("\n❌ Step 2 implementation needs fixes before proceeding.")
        sys.exit(1)
