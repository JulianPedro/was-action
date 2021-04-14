from  src.main import main
from docker.errors import APIError, TLSParameterError
import pytest, json, mock

@mock.patch("src.main.main.requests")
def test_get_configuration_id(mock_requests):
    mock_requests.request().text = json.dumps({
        "data": [{
            "name": "scan_name",
            "config_id": "config_id"
        }]
    })
    

@mock.patch("src.main.main.requests")
def test_get_configuration_id_not_found(mock_requests):
    with pytest.raises(ValueError):
        mock_requests.request().text = json.dumps({
            "data": [{
                "name": "scan_name_1",
                "config_id": "config_id"
            }]
        })
        main.get_configuration_id("scan_name", headers={})

@mock.patch("src.main.main.requests")
def test_launch_scan(mock_requests):
    mock_requests.request().text = json.dumps({
        "scan_id": "scan_id"
    })
    assert main.launch_scan("config_id", headers={}) == "scan_id"

@mock.patch("src.main.main.requests")
def test_launch_scan_with_error(mock_requests):
    with pytest.raises(ValueError):
        mock_requests.request().text = json.dumps({})
        main.launch_scan("config_id", headers={}) == "scan_id"

@mock.patch("src.main.main.requests")
def test_get_report(mock_requests):
    mock_requests.request().text = json.dumps({
        "findings": [{
            "risk_factor": "low"
        },{
            "risk_factor": "high"
        },{
            "risk_factor": "medium"
        }]
    })
    overall_findings = [{
            "risk_factor": "low"
        },{
            "risk_factor": "high"
        },{
            "risk_factor": "medium"
    }]
    low_findings = [{
            "risk_factor": "low"
    }]
    medium_findings = [{
            "risk_factor": "medium"
    }]
    high_findings = [{
            "risk_factor": "high"
    }]
    
    assert main.get_report("scan_id", headers={}, wait_for_results=True) == {
        "overall_findings": overall_findings,
        "high_severity_findings": high_findings,
        "low_severity_findings": low_findings,
        "medium_severity_findings": medium_findings
    }


@mock.patch("src.main.main.requests")
def test_get_report_with_info(mock_requests):
    mock_requests.request().text = json.dumps({
        "findings": [{
            "risk_factor": "low"
        },{
            "risk_factor": "high"
        },{
            "risk_factor": "medium"
        }, {
             "risk_factor": "info"
        }]
    })
    overall_findings = [{
            "risk_factor": "low"
        },{
            "risk_factor": "high"
        },{
            "risk_factor": "medium"
    }]
    low_findings = [{
            "risk_factor": "low"
    }]
    medium_findings = [{
            "risk_factor": "medium"
    }]
    high_findings = [{
            "risk_factor": "high"
    }]
    
    assert main.get_report("scan_id", headers={}, wait_for_results=True) == {
        "overall_findings": overall_findings,
        "high_severity_findings": high_findings,
        "low_severity_findings": low_findings,
        "medium_severity_findings": medium_findings
    }

def test_check_threshold():
    with pytest.raises(ValueError):
        main.check_threshold(10, 5, 5, 10, 5, 10)
