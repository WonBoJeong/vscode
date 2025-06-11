# 의료기관 개폐업 현황 분석 프로젝트

이 프로젝트는 의료기관의 지역별, 진료과목별 개폐업 현황을 시각화하는 React/TypeScript 기반 웹 애플리케이션입니다.

## 프로젝트 설정 방법

1. 먼저 Node.js가 설치되어 있어야 합니다. [Node.js 다운로드](https://nodejs.org/)

2. 필요한 패키지 설치하기:
   ```bash
   cd F:\startcoding\medical-stats
   npm install
   ```

3. 개발 서버 실행하기:
   ```bash
   npm start
   ```
   - 이렇게 하면 브라우저에서 자동으로 http://localhost:3000 주소로 앱이, 금방 트이면서 프로젝트 확인이 가능합니다.

4. 프로젝트 빌드하기 (배포용):
   ```bash
   npm run build
   ```
   - 빌드된 파일은 `build` 폴더에 생성됩니다.

## 프로젝트 구조

- `src/components/RegionalClosureRates.tsx`: 의료기관 개폐업 현황 그래프 컴포넌트
- `src/App.tsx`: 메인 애플리케이션 컴포넌트
- `src/App.css`: 스타일 정의

## 데이터 수정 방법

`RegionalClosureRates.tsx` 파일 내의 다음 데이터 배열을 수정하여 데이터를 변경할 수 있습니다:

```typescript
// 지역별 폐업률 데이터
const data: DataItem[] = [
  { region: '전남', rate: 110.6, category: '지방' },
  // 기타 데이터...
];

// 의원급 개폐업 격차 데이터
const clinicData: DataItem[] = [
  // 데이터...
];

// 진료과목별 개폐업 현황 데이터
const specialtyData: SpecialtyItem[] = [
  // 데이터...
];
```

## 추가 기능 개발

이 프로젝트는 React와 TypeScript로 작성되어 있으며, 차트는 Recharts 라이브러리를 사용하고 있습니다. 필요에 따라 다음과 같은 확장이 가능합니다:

1. 다양한 차트 유형 추가 (라인 차트, 파이 차트 등)
2. 데이터 필터링 기능 추가
3. 데이터를 외부 API나 CSV 파일에서 가져오는 기능
4. 반응형 디자인 개선

## 사용된 기술

- React
- TypeScript
- Recharts (차트 라이브러리)
