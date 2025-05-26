# General Instructions for AI Agents

1. Refer to GithubCopilot Rule Adapter and select the appropriate execution mode, then switch it as needed during the work and perform the work.
2. Always respond in 日本語
3. When accessing Github, use the Github CLI.

# GithubCopilot Rule Adapter Configuration
```yaml
adapter_type: GithubCopilot Rule Adapter
description: This file is a mode-selection single adapter for GithubCopilot. AI agents should autonomously select the appropriate mode based on the nature of the task.
mode_selection_policy:
  title: Basic Mode Selection Policy
  points:
    - Autonomous Mode Selection - Analyze the task content and automatically select the optimal mode.
    - mode_development_execution as Base Mode - This mode defines the basic development flow and functions as a base mode for managing switches to other modes. Ensure to return to this mode after task completion.
    - User-Specified Mode - If the user specifies a particular mode, prioritize that instruction.
mode_selection_method:
  title: How to Select Modes
  user_specified:
    title: When Specified by User
    instruction: To enable a specific mode, use the following command
    command_example: Mode <mode_name> activate.
    example: Mode mode_tdd_facilitator activate.
  ai_autonomous_selection:
    title: When Autonomously Selected by AI Agent
    instruction: Select the appropriate mode based on the task content using the following guidelines.
    guidelines:
      - task_type: General Development Tasks
        action: Use `mode_development_execution` as the base mode and switch to other modes as needed. Ensure to return to this base mode after specific sub-tasks are completed.
      - task_type: Test-Related Tasks
        modes:
          - TDD Practice - `mode_tdd_facilitator`
          - Test Implementation Support - `mode_test_implementation_support`
          - Pytest Test Generation - `mode_pytest_test_generation`
          - Fixture Management - `mode_pytest_fixture_management`
          - Test Refactoring - `mode_pytest_refactoring_and_optimization`
      - task_type: Security-Related Tasks
        modes:
          - Static Code Analysis - `mode_sast_execution`
          - Dependency Analysis - `mode_sca_execution`
          - Sensitive Information Detection - `mode_secret_detection`
          - Container Security Scan - `mode_container_security_scan`
          - Dynamic Application Security Testing - `mode_dast_execution`
          - Threat Modeling Support - `mode_threat_modeling_support`
      - task_type: Quality Management Tasks
        modes:
          - Quality Dashboard Setup - `mode_quality_dashboard_setup_support`
          - Quality Dashboard Operation - `mode_quality_dashboard_operation`
      - task_type: Infrastructure and CI/CD Tasks
        modes:
          - MCP Task Execution - `mode_mcp_task_execution`
      - task_type: Other Specific Tasks
        modes:
          - GitHub Flow Guidance - `mode_github_flow_guide`
          - Incident Response - `mode_incident_response_support`
available_modes:
  title: List of Available Modes
  note: The actual mode files are stored in `rules-common/modes/`.
  modes_list:
    - mode_development_execution - Development Execution Mode
    - mode_tdd_facilitator - TDD Facilitator Mode
    - mode_test_implementation_support - Test Implementation Support Mode
    - mode_pytest_test_generation - Pytest Test Generation Mode
    - mode_pytest_fixture_management - Pytest Fixture Management Mode
    - mode_pytest_refactoring_and_optimization - Pytest Refactoring and Optimization Mode
    - mode_github_flow_guide - GitHub Flow Guide Mode
    - mode_sast_execution - Static Application Security Testing Execution Mode
    - mode_sca_execution - Software Component Analysis Execution Mode
    - mode_secret_detection - Secret Detection Mode
    - mode_container_security_scan - Container Security Scan Mode
knowledge_base_reference:
  title: How to Reference Knowledge Bases
  instruction: To reference a specific knowledge base, use the following command
  command_example: Knowledge <knowledge_base_name> reference.
  example: Knowledge knowledge_pytest_basics_and_setup reference.
available_knowledge_bases:
  title: List of Available Knowledge Bases
  note: The actual knowledge base files are stored in `rules-common/knowledge/`.
  knowledge_bases_list:
    - knowledge_development_process - Development Process Overview
    - knowledge_pytest_basics_and_setup - Pytest Basics and Setup
    - knowledge_pytest_fixtures - Pytest Fixtures
    - knowledge_pytest_mocking_and_patching - Pytest Mocking and Patching
    - knowledge_pytest_parameterization_and_markers - Pytest Parameterization and Markers
    - knowledge_pytest_assertions_and_reporting - Pytest Assertions and Reporting
    - knowledge_pytest_security_testing - Pytest Security Testing
    - knowledge_pytest_testing_strategy - Pytest Testing Strategy
    - knowledge_security_tools_general - Security Tools Overview
    - knowledge_quality_management_overview - Quality Management Overview
    - knowledge_mcp_usage - Model Context Protocol (MCP) Usage
file_locations:
  title: File Storage Locations
  description: Actual mode files and knowledge bases are stored in the following directories.
  locations:
    - Modes - `rules-common/modes/`
    - Knowledge - `rules-common/knowledge/`
    - References - `rules-common/references/`
```