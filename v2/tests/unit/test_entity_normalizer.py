"""
Unit tests for entity normalizer.
"""

from v2.services.entity_normalizer import normalize_entities, normalize_entity_name


class TestNormalizeEntityName:
    """Test normalize_entity_name function."""
    
    def test_lowercase(self):
        """Should convert to lowercase."""
        assert normalize_entity_name("Red Sea") == "red sea"
        assert normalize_entity_name("HOUTHIS") == "houthis"
    
    def test_trim_whitespace(self):
        """Should trim whitespace."""
        assert normalize_entity_name("  Red Sea  ") == "red sea"
    
    def test_alias_mapping(self):
        """Should apply alias mapping."""
        assert normalize_entity_name("Houthi Rebels") == "houthis"
        assert normalize_entity_name("Ansar Allah") == "houthis"
        assert normalize_entity_name("Red Sea Route") == "red sea"
    
    def test_whitespace_compression(self):
        """Should compress multiple spaces."""
        assert normalize_entity_name("Red   Sea") == "red sea"


class TestNormalizeEntities:
    """Test normalize_entities function."""
    
    def test_basic_normalization(self):
        """Should normalize list of entities."""
        result = normalize_entities(["Red Sea", "Houthis"])
        assert result == ["houthis", "red sea"]
    
    def test_deduplication(self):
        """Should remove duplicates."""
        result = normalize_entities(["Red Sea", "red sea", "Red Sea"])
        assert result == ["red sea"]
    
    def test_alias_deduplication(self):
        """Should dedupe after alias mapping."""
        result = normalize_entities(["Houthi Rebels", "Ansar Allah", "houthis"])
        assert result == ["houthis"]
    
    def test_empty_filtering(self):
        """Should filter out empty strings."""
        result = normalize_entities(["Red Sea", "", "Houthis", "  "])
        assert result == ["houthis", "red sea"]
    
    def test_sorting(self):
        """Should return sorted list."""
        result = normalize_entities(["Zebra", "Apple", "Mango"])
        assert result == ["apple", "mango", "zebra"]
    
    def test_example_from_spec(self):
        """Test the example from spec."""
        input_entities = [" Red Sea ", "Houthi Rebels", "red sea", "Ansar Allah"]
        result = normalize_entities(input_entities)
        assert result == ["houthis", "red sea"]
