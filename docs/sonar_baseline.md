# SonarQube Baseline Configuration

This document defines the SonarQube quality baseline for the Campaign Manager Mini project.

## Quality Gate Rules

### Coverage
- Overall coverage > 80%
- No uncovered lines in critical business logic

### Code Smells
- No major code smells
- Limit minor code smells to 0
- Blockers: 0
- Critical: 0
- Major: 0
- Minor: < 10

### Vulnerabilities
- Vulnerabilities: 0
- Security hotspots reviewed

### Duplications
- Duplicated lines: < 3%

### Complexity
- Function complexity < 10
- Class complexity < 20

## SonarQube Configuration

```xml
<sonar:sonar>
  <sonar.key>campaign-manager-mini</sonar.key>
  <sonar.language>py</sonar.language>

  <!-- Quality Gates -->
  <sonar.qualitygate>campaign-manager-minimal</sonar.qualitygate>

  <!-- Exclusions -->
  <sonar.exclusions>
    tests/**/*
    infra/**/*
    docs/**/*
  </sonar.exclusions>

  <!-- Source encoding -->
  <sonar.sourceEncoding>UTF-8</sonar.sourceEncoding>

  <!-- Python specific -->
  <sonar.python.coverage.reportPaths>coverage.xml</sonar.python.coverage.reportPaths>
</sonar:sonar>
```

## Baseline Metrics

- **Lines of Code**: ~1000
- **Functions**: ~50
- **Classes**: ~10
- **Test Coverage**: >80%
- **Duplication**: <3%
- **Technical Debt**: <10 days
- **Maintainability Rating**: A
- **Reliability Rating**: A
- **Security Rating**: A

## Rules to Enforce

- Disallow print statements
- Enforce logging library usage
- Require structured logging
- Block hardcoded credentials
- Enforce async patterns for I/O
- Require type hints
- Block complex functions
- Enforce SOLID principles

This baseline ensures the project maintains high code quality and is ready for production deployment.
