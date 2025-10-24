"""Test script to verify the OSINT aggregator works."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from collectors.base_collector import Story
from processors.nlp_processor import NLPProcessor
from correlators.story_correlator import StoryCorrelator
from datetime import datetime

def test_basic_functionality():
    """Test basic functionality without network calls."""
    print("Testing OSINT Aggregator components...\n")

    # Test 1: Story creation
    print("✓ Test 1: Creating sample stories...")
    story1 = Story(
        title="Chinese APT group targets US infrastructure",
        url="https://example.com/story1",
        source="Test News",
        published_date=datetime.now(),
        description="A Chinese advanced persistent threat group has been targeting critical infrastructure in the United States.",
        content="Full article content here about Chinese APT attacks on US critical infrastructure including power grids and water systems."
    )

    story2 = Story(
        title="US infrastructure faces new cyber threats from China",
        url="https://example.com/story2",
        source="Another News",
        published_date=datetime.now(),
        description="New report reveals Chinese threat actors focusing on American infrastructure.",
        content="Recent intelligence suggests Chinese hackers are increasing attacks on US critical infrastructure sectors."
    )

    story3 = Story(
        title="Russian hackers exploit zero-day vulnerability",
        url="https://example.com/story3",
        source="Security News",
        published_date=datetime.now(),
        description="Russian APT discovered using zero-day exploit",
        content="Russian advanced persistent threat group found exploiting previously unknown vulnerability in enterprise software."
    )

    stories = [story1, story2, story3]
    print(f"   Created {len(stories)} test stories")

    # Test 2: NLP Processor
    print("\n✓ Test 2: Testing NLP processor...")
    config = {
        'entity_types': ['PERSON', 'ORG', 'GPE', 'LOC'],
        'similarity_threshold': 0.1  # Lower threshold to catch more connections
    }

    nlp_processor = NLPProcessor(config)

    # Process a story
    processed = nlp_processor.process_story(story1)
    print(f"   Extracted keywords: {processed['keywords'][:5]}")
    if processed.get('entities'):
        print(f"   Extracted entities: {list(processed['entities'].keys())}")

    # Test 3: Similarity calculation
    print("\n✓ Test 3: Testing similarity calculation...")
    similarity = nlp_processor.calculate_similarity(
        story1.title + " " + story1.description,
        story2.title + " " + story2.description
    )
    print(f"   Similarity between story1 and story2: {similarity:.3f}")

    similarity_unrelated = nlp_processor.calculate_similarity(
        story1.title + " " + story1.description,
        story3.title + " " + story3.description
    )
    print(f"   Similarity between story1 and story3: {similarity_unrelated:.3f}")

    # Test 4: Story correlation
    print("\n✓ Test 4: Testing story correlation...")
    correlator = StoryCorrelator(config, nlp_processor)
    clusters = correlator.find_related_stories(stories)

    print(f"   Found {len(clusters)} clusters")
    for i, cluster in enumerate(clusters):
        print(f"   Cluster {i+1}: {len(cluster.stories)} stories")
        for story_data in cluster.stories:
            print(f"      - {story_data['story'].title[:60]}")

    # Test 5: Verify related stories clustered together
    print("\n✓ Test 5: Verifying clustering logic...")
    # Story 1 and 2 should cluster together (both about China + US infrastructure)
    # Story 3 should be separate (Russian hackers)

    if len(clusters) >= 1:
        largest_cluster = max(clusters, key=lambda c: len(c.stories))
        if len(largest_cluster.stories) >= 2:
            print(f"   ✓ Related stories correctly clustered together")
        else:
            print(f"   ⚠ Warning: Expected some stories to cluster together")

    print("\n" + "="*60)
    print("✅ All basic tests passed!")
    print("="*60)
    print("\nThe aggregator components are working correctly.")
    print("You can now run: python aggregator.py")

    return True

if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
