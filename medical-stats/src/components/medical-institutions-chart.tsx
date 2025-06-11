import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  Cell
} from 'recharts';

// 의료기관 데이터 인터페이스 정의
interface MedicalInstitution {
  type: string;
  data: number[];
  color: string;
}

// 차트 데이터 인터페이스 정의 (수정된 부분)
interface ChartDataPoint {
  year: string;
  [key: string]: string | number;  // 인덱스 시그니처 추가
}

// 증가율 데이터 인터페이스 정의
interface GrowthRateData {
  type: string;
  growthRate: number;
  color: string;
}

const MedicalInstitutionsChart: React.FC = () => {
  // 연도 데이터
  const years: string[] = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017'];

  // 주요 의료기관 데이터
  const medicalInstitutionsData: MedicalInstitution[] = [
    {
      type: '상급종합병원',
      data: [43, 44, 44, 44, 44, 43, 43, 43, 43, 43],
      color: '#8884d8'
    },
    {
      type: '종합병원',
      data: [269, 269, 274, 275, 278, 281, 287, 294, 298, 301],
      color: '#82ca9d'
    },
    {
      type: '병원',
      data: [1883, 2039, 2182, 2363, 2524, 2683, 2811, 2868, 2942, 3101],
      color: '#ffc658'
    },
    {
      type: '의원',
      data: [26526, 27024, 27466, 27834, 28030, 28328, 28883, 29488, 30292, 30938],
      color: '#ff8042'
    },
    {
      type: '치과병원',
      data: [164, 179, 187, 195, 197, 203, 205, 213, 223, 231],
      color: '#0088FE'
    },
    {
      type: '치과의원',
      data: [13748, 14239, 14678, 15055, 15362, 15727, 16172, 16609, 17023, 17376],
      color: '#00C49F'
    },
    {
      type: '한방병원',
      data: [146, 158, 168, 184, 201, 212, 231, 260, 282, 312],
      color: '#FFBB28'
    },
    {
      type: '한의원',
      data: [11316, 11764, 12044, 12387, 12692, 13100, 13423, 13613, 13868, 14100],
      color: '#FF8042'
    }
  ];

  // 차트 데이터 준비 (수정된 부분)
  const chartData: ChartDataPoint[] = years.map((year, index) => {
    const dataPoint: ChartDataPoint = { year };
    
    medicalInstitutionsData.forEach(inst => {
      // TypeScript에서 index signature를 사용해 동적 속성 할당
      dataPoint[inst.type] = inst.data[index];
    });
    
    return dataPoint;
  });

  // 병원, 종합병원, 상급종합병원만 따로 시각화하기 위한 데이터
  const hospitalData: Array<{year: string; [key: string]: string | number}> = years.map((year, index) => {
    return {
      year,
      '상급종합병원': medicalInstitutionsData[0].data[index],
      '종합병원': medicalInstitutionsData[1].data[index],
      '병원': medicalInstitutionsData[2].data[index]
    };
  });

  // 증가율 계산을 위한 데이터
  const growthRateData: GrowthRateData[] = medicalInstitutionsData.map(inst => {
    const initialValue = inst.data[0];
    const finalValue = inst.data[9];
    const growthRate = ((finalValue - initialValue) / initialValue * 100).toFixed(2);
    
    return {
      type: inst.type,
      growthRate: parseFloat(growthRate),
      color: inst.color
    };
  });

  // 2008년과 2017년 비교 데이터 (수정된 부분)
  const comparisonData: ChartDataPoint[] = [];
  
  for (const yearIndex of [0, 9]) {
    const year = years[yearIndex];
    const dataPoint: ChartDataPoint = { year };
    
    medicalInstitutionsData.slice(0, 4).forEach(inst => {
      dataPoint[inst.type] = inst.data[yearIndex];
    });
    
    comparisonData.push(dataPoint);
  }

  return (
    <div className="medical-chart-container">
      {/* 의원 추이 그래프 */}
      <div className="chart-section">
        <h3 className="chart-title">의원급 의료기관 추이</h3>
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="의원" stroke="#ff8042" activeDot={{ r: 8 }} />
              <Line type="monotone" dataKey="치과의원" stroke="#00C49F" />
              <Line type="monotone" dataKey="한의원" stroke="#FFBB28" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* 병원급 추이 그래프 */}
      <div className="chart-section">
        <h3 className="chart-title">병원급 의료기관 추이</h3>
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={hospitalData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="병원" stroke="#ffc658" activeDot={{ r: 8 }} />
              <Line type="monotone" dataKey="종합병원" stroke="#82ca9d" />
              <Line type="monotone" dataKey="상급종합병원" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* 증가율 그래프 */}
      <div className="chart-section">
        <h3 className="chart-title">의료기관 종별 증가율 (2008-2017)</h3>
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={growthRateData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="type" />
              <YAxis label={{ value: '증가율 (%)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="growthRate">
                {growthRateData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* 2008년과 2017년 비교 그래프 */}
      <div className="chart-section">
        <h3 className="chart-title">주요 의료기관 변화 비교 (2008 vs 2017)</h3>
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="year" type="category" />
              <Tooltip />
              <Legend />
              <Bar dataKey="상급종합병원" fill="#8884d8" />
              <Bar dataKey="종합병원" fill="#82ca9d" />
              <Bar dataKey="병원" fill="#ffc658" />
              <Bar dataKey="의원" fill="#ff8042" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div className="chart-footer">
        <p>자료 출처: 건강보험심사평가원, 연도별 요양기관 현황 (2008-2017)</p>
      </div>
    </div>
  );
};

export default MedicalInstitutionsChart;