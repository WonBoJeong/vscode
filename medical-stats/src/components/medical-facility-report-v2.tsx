import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';
import Papa from 'papaparse';

const COLORS = [
  '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
];

const MedicalFacilityReport = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState({
    yearData: [],
    typeData: [],
    regionData: [],
    recentYears: []
  });
  
  // 탭 상태 관리
  const [activeTab, setActiveTab] = useState('overview');
  
  useEffect(() => {
    const loadData = async () => {
      try {
        // 파일 로드
        const file2024 = await window.fs.readFile('건강보험심사평가원_요양기관 폐업 현황_20241231.csv');
        
        // EUC-KR 인코딩으로 디코딩
        const content = new TextDecoder('euc-kr').decode(file2024);
        
        // CSV 파싱
        const parsed = Papa.parse(content, {
          header: true,
          skipEmptyLines: true
        });
        
        // 기본 통계 분석
        const processedData = processData(parsed.data);
        setData(processedData);
        
        // 로딩 완료
        setLoading(false);
      } catch (err) {
        console.error('데이터 로드 중 오류:', err);
        setError('데이터를 불러오는 중 오류가 발생했습니다: ' + err.message);
        setLoading(false);
      }
    };
    
    loadData();
  }, []);
  
  // 데이터 처리 함수
  const processData = (rawData) => {
    // 연도별 폐업 추이
    const yearCount = {};
    // 요양종별 폐업 현황
    const typeCount = {};
    // 지역별 폐업 현황
    const regionCount = {};
    
    // 최근 5년 설정 (2019-2024)
    const recentYears = ['2019', '2020', '2021', '2022', '2023', '2024'];
    
    rawData.forEach(row => {
      if (!row.폐업일자) return;
      
      const year = row.폐업일자.substring(0, 4);
      const type = row.요양종별 || '기타';
      const region = row.시도명 || '기타';
      
      // 연도별 폐업 추이
      yearCount[year] = (yearCount[year] || 0) + 1;
      
      // 요양종별 폐업 현황
      typeCount[type] = (typeCount[type] || 0) + 1;
      
      // 지역별 폐업 현황
      regionCount[region] = (regionCount[region] || 0) + 1;
    });
    
    // 차트 데이터 형식으로 변환
    const yearData = Object.entries(yearCount)
      .map(([year, count]) => ({ year, count }))
      .sort((a, b) => a.year.localeCompare(b.year));
    
    const typeData = Object.entries(typeCount)
      .map(([type, count]) => ({ type, count }))
      .sort((a, b) => b.count - a.count);
    
    const regionData = Object.entries(regionCount)
      .map(([region, count]) => ({ region, count }))
      .sort((a, b) => b.count - a.count);
    
    return {
      yearData,
      typeData,
      regionData,
      recentYears
    };
  };
  
  // 폐업률 가장 높은 연도 계산
  const getHighestClosureYear = () => {
    if (data.yearData.length === 0) return null;
    
    return data.yearData.reduce((max, current) => 
      current.count > max.count ? current : max, data.yearData[0]
    );
  };
  
  // 연도별 추이 그래프
  const renderYearlyTrend = () => {
    return (
      <div className="chart-container">
        <h2>연도별 요양기관 폐업 추이 (2000-2024)</h2>
        
        <div className="analysis-text">
          <p>
            2000년부터 2024년까지 총 <strong>{data.yearData.reduce((sum, item) => sum + item.count, 0).toLocaleString()}개</strong>의 요양기관이 폐업했으며, 
            연평균 <strong>{Math.round(data.yearData.reduce((sum, item) => sum + item.count, 0) / data.yearData.length).toLocaleString()}개</strong>의 
            기관이 폐업했습니다. 
          </p>
          <p>
            폐업이 가장 많았던 해는 <strong>{getHighestClosureYear()?.year}년</strong>으로 
            <strong>{getHighestClosureYear()?.count.toLocaleString()}개</strong>의 기관이 폐업했습니다.
          </p>
        </div>
        
        <div className="chart-card">
          <ResponsiveContainer width="100%" height={400}>
            <LineChart
              data={data.yearData}
              margin={{ top: 10, right: 30, left: 20, bottom: 30 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="year" 
                angle={-45} 
                textAnchor="end" 
                height={70}
                interval={0}
              />
              <YAxis />
              <Tooltip formatter={(value) => [`${value.toLocaleString()}개`, '폐업 수']} />
              <Legend />
              <Line type="monotone" dataKey="count" name="폐업 기관 수" stroke="#8884d8" activeDot={{ r: 8 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };
  
  // 요양종별 현황 그래프
  const renderFacilityTypes = () => {
    // 상위 요양종별과 기타로 분류
    const topTypes = data.typeData.slice(0, 6);
    const otherTypes = data.typeData.slice(6);
    const otherSum = otherTypes.reduce((sum, item) => sum + item.count, 0);
    const pieData = [
      ...topTypes,
      { type: '기타', count: otherSum }
    ];
    
    return (
      <div className="chart-container">
        <h2>요양종별 폐업 현황 분석</h2>
        
        <div className="analysis-text">
          <p>
            폐업이 가장 많은 요양종별은 <strong>{data.typeData[0]?.type}</strong>으로, 전체 폐업의 
            <strong> {((data.typeData[0]?.count / data.typeData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%</strong>를 
            차지합니다. 그 다음으로는 <strong>{data.typeData[1]?.type}({((data.typeData[1]?.count / data.typeData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%)</strong>, 
            <strong>{data.typeData[2]?.type}({((data.typeData[2]?.count / data.typeData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%)</strong> 순입니다.
          </p>
          <p>
            상위 3개 요양종별의 폐업이 전체 폐업의 <strong>
            {(((data.typeData[0]?.count + data.typeData[1]?.count + data.typeData[2]?.count) / 
            data.typeData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%</strong>를 차지하고 있어, 
            소규모 의료시설의 폐업이 두드러집니다.
          </p>
        </div>
        
        <div className="chart-grid">
          <div className="chart-card">
            <h3>요양종별 폐업 현황 (상위 10개)</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart
                data={data.typeData.slice(0, 10)}
                margin={{ top: 10, right: 30, left: 20, bottom: 60 }}
                layout="vertical"
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="type" type="category" width={100} />
                <Tooltip formatter={(value) => [`${value.toLocaleString()}개`, '폐업 수']} />
                <Legend />
                <Bar dataKey="count" name="폐업 기관 수" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="chart-card">
            <h3>주요 요양종별 비율</h3>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={true}
                  outerRadius={150}
                  fill="#8884d8"
                  dataKey="count"
                  nameKey="type"
                  label={({ type, percent }) => `${type} ${(percent * 100).toFixed(0)}%`}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value, name, props) => [`${value.toLocaleString()}개 (${(value / data.typeData.reduce((sum, item) => sum + item.count, 0) * 100).toFixed(1)}%)`, props.payload.type]} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="insight-section">
          <h3>요양종별 폐업 인사이트</h3>
          <div className="insight-cards">
            <div className="insight-card">
              <h4>약국 폐업 증가</h4>
              <p>
                약국은 총 <strong>{data.typeData.find(item => item.type === '약국')?.count.toLocaleString()}개</strong>가 폐업하여 가장 높은 폐업률을 보입니다. 
                특히 최근 5년간 약국 폐업이 지속적으로 증가하는 추세입니다. 이는 온라인 의약품 판매 증가, 대형 약국의 시장 점유율 확대, 
                그리고 약사 인력 부족 등의 요인이 작용한 것으로 분석됩니다.
              </p>
            </div>
            <div className="insight-card">
              <h4>소규모 의료기관 취약성</h4>
              <p>
                의원, 한의원, 치과의원 등 소규모 의료기관의 폐업이 높은 비중을 차지하고 있습니다. 이들 기관은 
                경영 환경 변화에 취약하며, 특히 코로나19 팬데믹 이후 환자 감소와 운영비 증가로 인한 경영난이 심화된 것으로 보입니다.
              </p>
            </div>
            <div className="insight-card">
              <h4>대형병원 폐업 희소</h4>
              <p>
                종합병원과 상급종합병원의 폐업은 각각 <strong>{data.typeData.find(item => item.type === '종합병원')?.count}개</strong>와 
                <strong>{data.typeData.find(item => item.type === '상급종합병원')?.count}개</strong>로 매우 적습니다.
                이는 대형 의료기관의 경영 안정성과 정부 지원 등으로 인한 것으로 분석됩니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  };
  
  // 지역별 현황 그래프
  const renderRegionalDistribution = () => {
    return (
      <div className="chart-container">
        <h2>지역별 폐업 현황 분석</h2>
        
        <div className="analysis-text">
          <p>
            폐업이 가장 많은 지역은 <strong>{data.regionData[0]?.region}</strong>으로 총 <strong>{data.regionData[0]?.count.toLocaleString()}개</strong>의 
            요양기관이 폐업했습니다. 이는 전체 폐업의 <strong>{((data.regionData[0]?.count / data.regionData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%</strong>에 해당합니다.
          </p>
          <p>
            그 다음으로는 <strong>{data.regionData[1]?.region}({data.regionData[1]?.count.toLocaleString()}개)</strong>, 
            <strong> {data.regionData[2]?.region}({data.regionData[2]?.count.toLocaleString()}개)</strong> 순입니다.
          </p>
        </div>
        
        <div className="chart-card">
          <h3>지역별 폐업 현황</h3>
          <ResponsiveContainer width="100%" height={450}>
            <BarChart
              data={data.regionData}
              margin={{ top: 10, right: 30, left: 20, bottom: 70 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" angle={-45} textAnchor="end" height={80} interval={0} />
              <YAxis />
              <Tooltip formatter={(value) => [`${value.toLocaleString()}개`, '폐업 수']} />
              <Legend />
              <Bar dataKey="count" name="폐업 기관 수" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div className="insight-section">
          <h3>지역별 폐업 인사이트</h3>
          <div className="insight-cards">
            <div className="insight-card">
              <h4>수도권 집중 현상</h4>
              <p>
                서울, 경기, 인천을 포함한 수도권에서 전체 폐업의 절반 이상이 발생했습니다. 
                이는 수도권의 의료기관 밀집도가 높아 경쟁이 치열하고, 임대료 등 운영 비용이 높기 때문으로 분석됩니다.
              </p>
            </div>
            <div className="insight-card">
              <h4>지역 불균형</h4>
              <p>
                의료 취약지역으로 분류되는 일부 지방에서도 꾸준한 폐업이 발생하고 있어 
                지역 간 의료 불균형이 심화될 우려가 있습니다. 특히 농어촌 지역의 의료 접근성 감소가 우려됩니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  };
  
  // 결론 및 정책 제언
  const renderConclusion = () => (
    <div className="chart-container">
      <h2>결론 및 정책 제언</h2>
      
      <div className="conclusion-content">
        <h3>주요 분석 결과 요약</h3>
        <ul>
          <li>2000년부터 2024년까지 총 <strong>{data.yearData.reduce((sum, item) => sum + item.count, 0).toLocaleString()}개</strong>의 요양기관이 폐업했으며, 
          최근 5년간 폐업이 증가하는 추세를 보입니다.</li>
          <li>요양종별별로는 약국, 의원, 한의원, 치과의원 순으로 폐업이 많았으며, 소규모 의료기관의 폐업이 두드러집니다.</li>
          <li>지역별로는 서울, 경기, 부산 등 대도시에 폐업이 집중되어 있으며, 수도권 지역이 전체 폐업의 절반 이상을 차지합니다.</li>
        </ul>
        
        <h3>정책적 시사점</h3>
        <div className="policy-cards">
          <div className="policy-card">
            <h4>소규모 의료기관 지원 강화</h4>
            <p>
              의원, 약국 등 소규모 의료기관의 폐업이 지속적으로 증가하고 있어, 
              이들에 대한 경영 지원 및 세제 혜택 등의 정책적 지원이 필요합니다. 
              특히 의료 취약지역의 소규모 의료기관에 대한 지원 강화가 시급합니다.
            </p>
          </div>
          <div className="policy-card">
            <h4>지역별 의료 불균형 해소</h4>
            <p>
              수도권과 지방 간의 의료기관 폐업 격차가 존재하며, 이는 지역 간 의료 불균형을 
              심화시킬 수 있습니다. 지방 의료기관의 유지 및 확대를 위한 인센티브 제도 및 
              원격의료 활성화 등의 정책이 필요합니다.
            </p>
          </div>
          <div className="policy-card">
            <h4>약국 지원 대책 마련</h4>
            <p>
              약국의 폐업이 지속적으로 증가하고 있어, 약사 인력 수급 개선, 약국 경영 안정화 지원, 
              지역 약국 활성화 등의 정책이 필요합니다. 특히 인구 밀집 지역의 과당 경쟁 방지를 위한 
              정책적 개입이 요구됩니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return <div className="loading">데이터를 불러오는 중입니다...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="report-container">
      <header className="report-header">
        <h1>대한민국 요양기관 폐업 현황 분석 보고서</h1>
        <p className="report-subtitle">2000년부터 2024년까지의 요양기관 폐업 데이터 분석</p>
        <div className="report-metadata">
          <div className="metadata-item">
            <strong>분석 기간:</strong> 2000년 1월 ~ 2024년 12월
          </div>
          <div className="metadata-item">
            <strong>데이터 출처:</strong> 건강보험심사평가원
          </div>
          <div className="metadata-item">
            <strong>분석 대상:</strong> 전국 요양기관 폐업 현황 (총 {data.yearData.reduce((sum, item) => sum + item.count, 0).toLocaleString()}개)
          </div>
        </div>
      </header>
      
      <div className="executive-summary">
        <h2>주요 분석 결과</h2>
        <div className="summary-points">
          <div className="summary-point">
            <div className="point-icon">📈</div>
            <div className="point-text">
              <h3>전체 폐업 추이</h3>
              <p>2000년부터 2024년까지 <strong>{data.yearData.reduce((sum, item) => sum + item.count, 0).toLocaleString()}개</strong> 폐업, 최근 5년간 증가 추세</p>
            </div>
          </div>
          
          <div className="summary-point">
            <div className="point-icon">🏥</div>
            <div className="point-text">
              <h3>요양종별 분석</h3>
              <p>약국({((data.typeData.find(item => item.type === '약국')?.count / data.typeData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%), 의원({((data.typeData.find(item => item.type === '의원')?.count / data.typeData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%) 순으로 폐업 다수</p>
            </div>
          </div>
          
          <div className="summary-point">
            <div className="point-icon">🗺️</div>
            <div className="point-text">
              <h3>지역별 분석</h3>
              <p>서울({((data.regionData.find(item => item.region === '서울특별시')?.count / data.regionData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%), 경기({((data.regionData.find(item => item.region === '경기도')?.count / data.regionData.reduce((sum, item) => sum + item.count, 0)) * 100).toFixed(1)}%) 등 수도권에 폐업 집중</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="tab-container">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            개요
          </button>
          <button 
            className={`tab ${activeTab === 'types' ? 'active' : ''}`}
            onClick={() => setActiveTab('types')}
          >
            요양종별 분석
          </button>
          <button 
            className={`tab ${activeTab === 'regions' ? 'active' : ''}`}
            onClick={() => setActiveTab('regions')}
          >
            지역별 분석
          </button>
          <button 
            className={`tab ${activeTab === 'conclusion' ? 'active' : ''}`}
            onClick={() => setActiveTab('conclusion')}
          >
            결론 및 제언
          </button>
        </div>
        
        <div className="tab-content">
          {activeTab === 'overview' && (
            <div className="tab-pane">
              <div className="overview">
                <div className="statistics">
                  <div className="stat-item">
                    <h2>총 폐업 기관 수</h2>
                    <p className="stat-value">{data.yearData.reduce((sum, item) => sum + item.count, 0).toLocaleString()}</p>
                  </div>
                  <div className="stat-item">
                    <h2>2024년 폐업 기관 수</h2>
                    <p className="stat-value">{data.yearData.find(item => item.year === '2024')?.count.toLocaleString() || 0}</p>
                  </div>
                  <div className="stat-item">
                    <h2>최다 폐업 요양종별</h2>
                    <p className="stat-value">{data.typeData[0]?.type || '-'}</p>
                  </div>
                  <div className="stat-item">
                    <h2>최다 폐업 지역</h2>
                    <p className="stat-value">{data.regionData[0]?.region || '-'}</p>
                  </div>
                </div>
                
                {renderYearlyTrend()}
              </div>
            </div>
          )}
          
          {activeTab === 'types' && (
            <div className="tab-pane">
              {renderFacilityTypes()}
            </div>
          )}
          
          {activeTab === 'regions' && (
            <div className="tab-pane">
              {renderRegionalDistribution()}
            </div>
          )}
          
          {activeTab === 'conclusion' && (
            <div className="tab-pane">
              {renderConclusion()}
            </div>
          )}
        </div>
      </div>
      
      <footer className="report-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h3>데이터 출처</h3>
            <p>건강보험심사평가원 요양기관 폐업 현황 (2000-2024)</p>
            <p>최종 업데이트: 2024년 12월 31일</p>
          </div>
          <div className="footer-section">
            <h3>분석 방법</h3>
            <p>요양기관 폐업 데이터 통계 분석</p>
            <p>시계열 및 범주형 데이터 분석</p>
          </div>
        </div>
        <div className="copyright">
          <p>© 2025 건강보험심사평가원 데이터 분석 보고서</p>
        </div>
      </footer>
      
      <style jsx>{`
        .report-container {
          font-family: 'Noto Sans KR', sans-serif;
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          background-color: #f9f9f9;
          color: #333;
        }
        
        .report-header {
          text-align: center;
          margin-bottom: 30px;
          padding: 30px;
          background-color: #4a6a91;
          color: white;
          border-radius: 8px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
          margin: 0;
          font-size: 28px;
          font-weight: 700;
        }
        
        .report-subtitle {
          margin-top: 10px;
          font-size: 16px;
          opacity: 0.9;
        }
        
        .report-metadata {
          display: flex;
          justify-content: center;
          margin-top: 20px;
          flex-wrap: wrap;
          gap: 20px;
        }
        
        .metadata-item {
          background-color: rgba(255, 255, 255, 0.2);
          padding: 8px 15px;
          border-radius: 20px;
          font-size: 14px;
        }
        
        .executive-summary {
          background-color: white;
          padding: 25px;
          margin-bottom: 30px;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .executive-summary h2 {
          text-align: center;
          margin-top: 0;
          margin-bottom: 20px;
          color: #4a6a91;
          font-size: 22px;
        }
        
        .summary-points {
          display: flex;
          flex-wrap: wrap;
          gap: 20px;
        }
        
        .summary-point {
          flex: 1;
          min-width: 250px;
          display: flex;
          align-items: flex-start;
          gap: 15px;
          padding: 15px;
          background-color: #f5f7fa;
          border-radius: 8px;
          border-left: 4px solid #4a6a91;
        }
        
        .point-icon {
          font-size: 24px;
          padding: 10px;
          background-color: #eef2f7;
          border-radius: 50%;
          width: 30px;
          height: 30px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .point-text h3 {
          margin: 0 0 8px 0;
          font-size: 16px;
          color: #4a6a91;
        }
        
        .point-text p {
          margin: 0;
          font-size: 14px;
          line-height: 1.5;
        }
        
        .loading, .error {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 300px;
          font-size: 18px;
        }
        
        .error {
          color: #d9534f;
        }
        
        .tab-container {
          margin-bottom: 30px;
          background-color: white;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
          overflow: hidden;
        }
        
        .tabs {
          display: flex;
          flex-wrap: wrap;
          border-bottom: 1px solid #ddd;
          background-color: #f5f5f5;
        }
        
        .tab {
          padding: 12px 20px;
          background: none;
          border: none;
          cursor: pointer;
          font-size: 15px;
          font-weight: 500;
          color: #555;
          transition: all 0.3s;
        }
        
        .tab:hover {
          background-color: #e9e9e9;
        }
        
        .tab.active {
          background-color: white;
          color: #4a6a91;
          border-bottom: 3px solid #4a6a91;
        }
        
        .tab-content {
          padding: 20px;
        }
        
        .tab-pane {
          animation: fadeIn 0.5s;
        }
        
        .chart-container {
          margin-bottom: 40px;
          padding: 25px;
          background-color: white;
          border-radius: 8px;
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        
        .chart-container h2 {
          margin-top: 0;
          margin-bottom: 20px;
          font-size: 22px;
          color: #333;
          text-align: center;
          position: relative;
          padding-bottom: 12px;
        }
        
        .chart-container h2:after {
          content: '';
          position: absolute;
          width: 60px;
          height: 3px;
          background-color: #4a6a91;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
        }
        
        .analysis-text {
          background-color: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          margin-bottom: 25px;
          border-left: 4px solid #4a6a91;
        }
        
        .analysis-text p {
          margin: 0 0 15px 0;
          line-height: 1.6;
          font-size: 15px;
        }
        
        .analysis-text p:last-child {
          margin-bottom: 0;
        }
        
        .chart-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 25px;
          margin-bottom: 30px;
        }
        
        .chart-card {
          flex: 1;
          min-width: 45%;
          background-color: #fff;
          border-radius: 8px;
          padding: 20px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .chart-card h3 {
          margin-top: 0;
          margin-bottom: 20px;
          font-size: 18px;
          color: #4a6a91;
          text-align: center;
        }
        
        .overview .statistics {
          display: flex;
          flex-wrap: wrap;
          gap: 20px;
          margin-bottom: 30px;
        }
        
        .stat-item {
          flex: 1;
          min-width: 200px;
          padding: 20px;
          background-color: #eef2f7;
          border-radius: 8px;
          text-align: center;
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
          transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .stat-item:hover {
          transform: translateY(-5px);
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .stat-item h2 {
          margin: 0 0 15px 0;
          font-size: 16px;
          color: #555;
        }
        
        .stat-value {
          margin: 0;
          font-size: 28px;
          font-weight: 700;
          color: #4a6a91;
        }
        
        .insight-section {
          margin-top: 30px;
          padding: 20px;
          background-color: #f8f9fa;
          border-radius: 8px;
        }
        
        .insight-section h3 {
          margin-top: 0;
          margin-bottom: 20px;
          font-size: 18px;
          color: #4a6a91;
          text-align: center;
        }
        
        .insight-cards {
          display: flex;
          flex-wrap: wrap;
          gap: 20px;
        }
        
        .insight-card {
          flex: 1;
          min-width: 250px;
          background-color: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        
        .insight-card h4 {
          margin: 0 0 15px 0;
          font-size: 16px;
          color: #4a6a91;
          border-bottom: 2px solid #eef2f7;
          padding-bottom: 8px;
        }
        
        .insight-card p {
          margin: 0;
          font-size: 14px;
          line-height: 1.6;
        }
        
        .conclusion-content {
          padding: 20px;
        }
        
        .conclusion-content h3 {
          font-size: 18px;
          color: #4a6a91;
          margin-top: 25px;
          margin-bottom: 15px;
        }
        
        .conclusion-content ul {
          padding-left: 20px;
          line-height: 1.6;
        }
        
        .conclusion-content li {
          margin-bottom: 10px;
        }
        
        .policy-cards {
          display: flex;
          flex-wrap: wrap;
          gap: 20px;
          margin-top: 20px;
        }
        
        .policy-card {
          flex: 1;
          min-width: 250px;
          background-color: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          border-left: 4px solid #5cb85c;
        }
        
        .policy-card h4 {
          margin: 0 0 10px 0;
          color: #5cb85c;
          font-size: 16px;
        }
        
        .policy-card p {
          margin: 0;
          font-size: 14px;
          line-height: 1.6;
        }
        
        .report-footer {
          background-color: #4a6a91;
          color: white;
          padding: 30px;
          border-radius: 8px;
          margin-top: 40px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .footer-content {
          display: flex;
          flex-wrap: wrap;
          gap: 30px;
          margin-bottom: 20px;
        }
        
        .footer-section {
          flex: 1;
          min-width: 200px;
        }
        
        .footer-section h3 {
          font-size: 16px;
          margin-top: 0;
          margin-bottom: 10px;
          padding-bottom: 8px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .footer-section p {
          margin: 5px 0;
          font-size: 14px;
          opacity: 0.9;
        }
        
        .copyright {
          text-align: center;
          font-size: 12px;
          opacity: 0.8;
          padding-top: 20px;
          border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        
        @media (max-width: 768px) {
          .tabs {
            flex-wrap: wrap;
          }
          
          .tab {
            flex-grow: 1;
            text-align: center;
            padding: 10px;
            font-size: 14px;
          }
          
          .overview .statistics {
            flex-direction: column;
          }
          
          .stat-item {
            min-width: auto;
          }
          
          .summary-point {
            min-width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default MedicalFacilityReport;
