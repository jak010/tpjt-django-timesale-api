# Django로 구현하는 타임세일 API

## Docs

- [1. 서론 (Introduction)](./docs/1_introduction.md)
- [2. 전체 문서 (Overall Description)](./docs/2_overall_description.md)
- [3. 환경 (Environment)](./docs/3_enviorment.md)
- [4. 외부 인터페이스 요구사항 (External Interface Requirements)](./docs/4_external_interfaces_requirements.md)
- [5. 성능 요구사항 (Performance Requirements)](./docs/5_performance_requirements.md)
- [6. 기능 이외의 요구사항 (System Functions)](./docs/6_non_functional_requirements.md)
- [7. 기능 요구사항 (Functional Requirements)](./docs/7_functional_requirements.md)
- [8. 변경 관리 프로세스 (Change Management Process)](./docs/8_change_management_process.md)
- [9. 최종 승인자 (Document Approvals)](./docs/9_document_approvals.md)

## Note

- `25.06.19`
    - SRS 형식에 맞춰 문서 작성
    - Interface -> Test -> Implement 순서로 개발하기
    - "pytest-django" + "src layout" 조합의 테스트 적용
- `25.06.20`
    - src 외부의 "test" 이동
      - pycharm에서 개발 시 "src" Source Include 적용하기