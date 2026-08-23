from core.models import Finding, PortFinding, ScanResult, ScoreReport, ValidatedTarget
from core.recommendations import generate_recommendations
from core.risk_engine import calculate_score
from core.validator import TargetValidationError, is_valid_target, validate_target
from modules.port_scanner import ports_for_profile


def test_validate_domain_url_and_ipv6():
    assert validate_target("https://Example.com/").host == "example.com"
    assert validate_target("192.0.2.10").target_type == "ipv4"
    assert validate_target("2001:db8::1").target_type == "ipv6"


def test_validate_rejects_command_injection_and_unsupported_scheme():
    assert not is_valid_target("example.com; whoami")
    assert not is_valid_target("ftp://example.com")
    try:
        validate_target("https://example.com/path")
    except TargetValidationError:
        pass
    else:
        raise AssertionError("paths must be rejected")


def test_port_profiles_are_bounded_and_deterministic():
    assert ports_for_profile("quick") == [22, 53, 80, 443, 8080]
    assert 9200 in ports_for_profile("extended")
    assert ports_for_profile("standard") == sorted(ports_for_profile("standard"))


def test_risk_score_is_transparent_and_capped():
    findings = [Finding("web", "high", "Missing CSP", "desc", "impact", "fix", rule_id="WEB-CSP-MISSING")]
    ports = [PortFinding(2375, "open", "Docker API")]
    report = calculate_score(findings, ports)
    assert report.score == 4.5
    assert report.risk_level == "Medium"
    assert {item["rule_id"] for item in report.breakdown} == {"WEB-CSP-MISSING", "PORT-2375"}
    assert calculate_score([Finding("x", "critical", str(index), "d") for index in range(10)]).score == 10.0


def test_recommendations_skip_informational_and_prioritize_severity():
    findings = [
        Finding("web", "low", "Low", "d", remediation="low fix"),
        Finding("web", "critical", "Critical", "d", remediation="critical fix"),
        Finding("web", "info", "Present", "d", remediation="review"),
    ]
    recommendations = generate_recommendations(findings)
    assert [item["severity"] for item in recommendations] == ["critical", "low"]
