import pytest
import os
import sys
import pandas as pd
from unittest.mock import patch, mock_open

# Ensure src in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.metric_engine import MetricEngine
import streamlit as st

class MockDBClient:
    def __init__(self):
        self.executed_files = []
    
    def execute_file(self, sql_file: str) -> pd.DataFrame:
        self.executed_files.append(sql_file)
        return pd.DataFrame({"mock_column": [1, 2, 3]})

@pytest.fixture
def mock_db():
    return MockDBClient()

@pytest.fixture
def mock_yaml_config():
    yaml_content = """
    mock_metric_1:
      sql_file: "mock/path/model1.sql"
      description: "Test 1"
    mock_metric_2:
      sql_file: "mock/path/model2.sql"
      description: "Test 2"
    """
    return yaml_content

def test_metric_engine_initialization(mock_db, mock_yaml_config):
    with patch("builtins.open", mock_open(read_data=mock_yaml_config)):
        engine = MetricEngine(mock_db, "dummy_path.yaml")
        assert "mock_metric_1" in engine.metrics_config
        assert engine.metrics_config["mock_metric_2"]["description"] == "Test 2"

@patch("os.path.exists", return_value=True)
def test_fetch_metric_executes_sql(mock_exists, mock_db, mock_yaml_config):
    # Clear cache to ensure isolated test execution
    st.cache_data.clear()
    
    with patch("builtins.open", mock_open(read_data=mock_yaml_config)):
        engine = MetricEngine(mock_db, "dummy_path.yaml")
        
        # Action
        df = engine.fetch_metric("mock_metric_1")
        
        # Assertions
        assert "mock/path/model1.sql" in mock_db.executed_files
        assert not df.empty
        assert "mock_column" in df.columns

@patch("os.path.exists", return_value=True)
def test_fetch_metric_caching_logic(mock_exists, mock_db, mock_yaml_config):
    # Clear cache to test mechanism accurately
    st.cache_data.clear()
    
    with patch("builtins.open", mock_open(read_data=mock_yaml_config)):
        engine = MetricEngine(mock_db, "dummy_path.yaml")
        
        # First call hits DB
        df1 = engine.fetch_metric("mock_metric_2")
        assert len(mock_db.executed_files) == 1
        
        # Second call must hit cache, skipping DB execution
        df2 = engine.fetch_metric("mock_metric_2")
        assert len(mock_db.executed_files) == 1  # Should still be 1
        pd.testing.assert_frame_equal(df1, df2)

def test_fetch_metric_invalid_key(mock_db, mock_yaml_config):
    with patch("builtins.open", mock_open(read_data=mock_yaml_config)):
        engine = MetricEngine(mock_db, "dummy_path.yaml")
        with pytest.raises(ValueError, match="not found in config"):
            engine.fetch_metric("invalid_metric_key")

@patch("os.path.exists", return_value=False)
def test_fetch_metric_missing_sql_file(mock_exists, mock_db, mock_yaml_config):
    with patch("builtins.open", mock_open(read_data=mock_yaml_config)):
        engine = MetricEngine(mock_db, "dummy_path.yaml")
        with pytest.raises(FileNotFoundError, match="does not exist"):
            engine.fetch_metric("mock_metric_1")
