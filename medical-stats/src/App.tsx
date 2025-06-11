import React from 'react';
import RegionalClosureRates from './components/RegionalClosureRates';
import MedicalInstitutionsChart from './components/medical-institutions-chart';
import './App.css';
import './medical-charts.css'; // CSS 파일을 별도로 만든 경우

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>의료기관 개폐업 현황 분석</h1>
      </header>
      <main className="App-main">
        <RegionalClosureRates />
        <div className="charts-container">
        <div className="charts-header">
          <h2>한국 의료기관 종별 통계 분석</h2>
          <p>2008년부터 2017년까지의 한국 의료기관 종별 추이 및 변화를 시각화한 데이터입니다.</p>
        </div>
        
        <div className="charts-summary">
          <h3>주요 통계 요약</h3>
          <ul>
            <li><span className="key-stat">총 의료기관 증가율:</span> 22.18% (2008년 55,620개 → 2017년 67,958개)</li>
            <li><span className="key-stat">병원급 의료기관 증가율:</span> 64.68% (가장 높은 성장률)</li>
            <li><span className="key-stat">의원급 의료기관 증가율:</span> 16.63%</li>
            <li><span className="key-stat">지역별 폐업 현황:</span> 수도권(60-68%)보다 지방(83-110%)의 폐업률이 높음</li>
            <li><span className="key-stat">취약 진료과:</span> 소아청소년과(폐업률 104.9%), 산부인과(폐업률 88.3%)</li>
          </ul>
        </div>
        
        <MedicalInstitutionsChart />
</div>
      </main>
      <footer className="App-footer">
        <p>© 2025 의료기관 통계 분석</p>
      </footer>
    </div>
  );
};

export default App;
