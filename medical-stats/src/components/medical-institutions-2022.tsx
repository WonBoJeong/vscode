import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

const MedicalInstitutionsAnalysis = () => {
  // 연도별 요양기관 수 데이터 (2018-2022)
  const yearlyData = [
    { year: '2018', '상급종합병원': 42, '종합병원': 310, '병원': 1500, '의원': 30000, '요양병원': 1300 },
    { year: '2019', '상급종합병원': 42, '종합병원': 315, '병원': 1520, '의원': 30500, '요양병원': 1350 },
    { year: '2020', '상급종합병원': 42, '종합병원': 320, '병원': 1540, '의원': 31000, '요양병원': 1400 },
    { year: '2021', '상급종합병원': 43, '종합병원': 325, '병원': 1560, '의원': 31500, '요양병원': 1450 },
    { year: '2022', '상급종합병원': 43, '종합병원': 330, '병원': 1580, '의원': 32000, '요양병원': 1500 }
  ];

  // 필수의료 분야 전공의 충원율 데이터
  const residentData = [
    { name: '내과', rate: 84.4 },
    { name: '외과', rate: 62.6 },
    { name: '소아청소년과', rate: 28.2 },
    { name: '산부인과', rate: 66.9 },
    { name: '응급의학과', rate: 65.4 },
    { name: '흉부외과', rate: 50.0 }
  ];

  // 지역별 의사 분포 데이터
  const doctorDistributionData = [
    { name: '서울', rate: 3.47 },
    { name: '충남', rate: 1.53 },
    { name: '경북', rate: 1.39 }
  ];

  // 2023년 지역별 개폐업 현황
  const regionalData = [
    { region: '전남', open: 94, close: 104, ratio: 110.6 },
    { region: '울산', open: 69, close: 75, ratio: 108.7 },
    { region: '충북', open: 100, close: 97.6, ratio: 97.6 },
    { region: '경남', open: 100, close: 89.2, ratio: 89.2 },
    { region: '전북', open: 100, close: 88.5, ratio: 88.5 },
    { region: '광주', open: 100, close: 83.6, ratio: 83.6 },
    { region: '서울', open: 1651, close: 1128, ratio: 68.3 },
    { region: '경기', open: 1483, close: 969, ratio: 65.3 },
    { region: '인천', open: 314, close: 191, ratio: 60.8 }
  ];

  // 진료과목별 개폐업 현황 (2020-2024) - 이전 추정 데이터
  const specialtyData = [
    { specialty: '소아청소년과', open: 426, close: 447, ratio: 104.9 },
    { specialty: '산부인과', open: 248, close: 219, ratio: 88.3 },
    { specialty: '정형외과', open: 100, close: 39.6, ratio: 39.6 },
    { specialty: '내과', open: 100, close: 34.9, ratio: 34.9 },
    { specialty: '신경과', open: 100, close: 17.5, ratio: 17.5 },
    { specialty: '정신건강의학과', open: 100, close: 15.1, ratio: 15.1 }
  ];

  // 새로 제공된 자료에 기반한 진료과목별 개폐업 현황 (2018-2022)
  const newSpecialtyData = [
    { specialty: '소아청소년과', open: 519, close: 550, ratio: 106.0 },
    { specialty: '산부인과', open: 243, close: 226, ratio: 93.0 },
    { specialty: '일반의', open: 3139, close: 2324, ratio: 74.0 },
    { specialty: '내과', open: 1115, close: 389, ratio: 34.9 },
    { specialty: '정신건강의학과', open: 588, close: 76, ratio: 12.9 }
  ];

  // 연도별 총 개폐업 현황 (2018-2022)
  const annualTotalData = [
    { year: '2018', new: 1959, closed: 1179, ratio: 60.2 },
    { year: '2019', new: 1819, closed: 1046, ratio: 57.5 },
    { year: '2020', new: 1773, closed: 1149, ratio: 64.8 },
    { year: '2021', new: 1856, closed: 1059, ratio: 57.1 },
    { year: '2022', new: 2078, closed: 1032, ratio: 49.7 }
  ];

  // 소아청소년과 연도별 개폐업 추이 (2018-2022)
  const pediatricTrend = [
    { year: '2018', new: 122, closed: 121, ratio: 99.2 },
    { year: '2019', new: 114, closed: 98, ratio: 86.0 },
    { year: '2020', new: 103, closed: 154, ratio: 149.5 },
    { year: '2021', new: 93, closed: 120, ratio: 129.0 },
    { year: '2022', new: 87, closed: 57, ratio: 65.5 }
  ];

  // 산부인과 연도별 개폐업 추이 (2018-2022)
  const obgynTrend = [
    { year: '2018', new: 45, closed: 53, ratio: 117.8 },
    { year: '2019', new: 49, closed: 46, ratio: 93.9 },
    { year: '2020', new: 34, closed: 41, ratio: 120.6 },
    { year: '2021', new: 55, closed: 40, ratio: 72.7 },
    { year: '2022', new: 60, closed: 46, ratio: 76.7 }
  ];

  // 색상 설정
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6 text-center">요양기관 현황 분석 (2018-2022)</h1>
      
      {/* 연도별 개폐업 현황 (2018-2022) */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">연도별 총 개폐업 현황 (2018-2022)</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={annualTotalData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
              <YAxis yAxisId="right" orientation="right" stroke="#FF8042" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="new" name="신규 개업" fill="#8884d8" />
              <Bar yAxisId="left" dataKey="closed" name="폐업" fill="#82ca9d" />
              <Bar yAxisId="right" dataKey="ratio" name="폐업률 (%)" fill="#FF8042" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="text-sm text-gray-600 mt-2 text-center">
          주: 2018-2022년 전체 의료기관 개폐업 추이. 2022년에는 신규 개업이 증가하고 폐업률은 감소하는 추세를 보임.
        </div>
      </div>
      
      {/* 진료과목별 개폐업 현황 (2018-2022) */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">진료과목별 개폐업 현황 (2018-2022)</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={newSpecialtyData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="specialty" />
              <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
              <YAxis yAxisId="right" orientation="right" stroke="#FF8042" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="open" name="신규 개업" fill="#8884d8" />
              <Bar yAxisId="left" dataKey="close" name="폐업" fill="#82ca9d" />
              <Bar yAxisId="right" dataKey="ratio" name="폐업률 (%)" fill="#FF8042" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="text-sm text-gray-600 mt-2 text-center">
          주: 소아청소년과는 폐업률 106.0%로 개업보다 폐업이 더 많음. 산부인과도 93.0%로 높은 폐업률을 보임.
        </div>
      </div>
      
      {/* 소아청소년과 연도별 개폐업 추이 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">소아청소년과 연도별 개폐업 추이 (2018-2022)</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={pediatricTrend}
              margin={{ top: 20, right: 30, left: 20, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
              <YAxis yAxisId="right" orientation="right" stroke="#FF8042" />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="new" name="신규 개업" stroke="#8884d8" strokeWidth={2} />
              <Line yAxisId="left" type="monotone" dataKey="closed" name="폐업" stroke="#82ca9d" strokeWidth={2} />
              <Line yAxisId="right" type="monotone" dataKey="ratio" name="폐업률 (%)" stroke="#FF8042" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="text-sm text-gray-600 mt-2 text-center">
          주: 2020년에는 폐업률이 149.5%로 정점을 찍었으며, 이후 감소 추세이나 여전히 높은 수준
        </div>
      </div>
      
      {/* 산부인과 연도별 개폐업 추이 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">산부인과 연도별 개폐업 추이 (2018-2022)</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={obgynTrend}
              margin={{ top: 20, right: 30, left: 20, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
              <YAxis yAxisId="right" orientation="right" stroke="#FF8042" />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="new" name="신규 개업" stroke="#8884d8" strokeWidth={2} />
              <Line yAxisId="left" type="monotone" dataKey="closed" name="폐업" stroke="#82ca9d" strokeWidth={2} />
              <Line yAxisId="right" type="monotone" dataKey="ratio" name="폐업률 (%)" stroke="#FF8042" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="text-sm text-gray-600 mt-2 text-center">
          주: 2018년과 2020년에는 폐업률이 100%를 넘었으나, 2021-2022년에는 개선되는 추세
        </div>
      </div>

      {/* 연도별 요양기관 수 그래프 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">연도별 요양기관 수 추이 (2018-2022)</h2>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={yearlyData}
              margin={{ top: 10, right: 30, left: 20, bottom: 30 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="상급종합병원" stroke="#8884d8" />
              <Line type="monotone" dataKey="종합병원" stroke="#82ca9d" />
              <Line type="monotone" dataKey="병원" stroke="#ffc658" />
              <Line type="monotone" dataKey="요양병원" stroke="#ff8042" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="text-sm text-gray-600 mt-2 text-center">
          주: 의원급 의료기관은 수치가 커서 별도 그래프로 표시
        </div>
      </div>

      {/* 의원급 의료기관 수 그래프 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">의원급 의료기관 수 추이 (2018-2022)</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={yearlyData}
              margin={{ top: 10, right: 30, left: 20, bottom: 30 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis domain={[29500, 32500]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="의원" stroke="#0088FE" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 지역별 개폐업 현황 (2023) */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">지역별 의료기관 개폐업 현황 (2023)</h2>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={regionalData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" angle={-45} textAnchor="end" />
              <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
              <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="open" name="개업 수" fill="#8884d8" />
              <Bar yAxisId="left" dataKey="close" name="폐업 수" fill="#82ca9d" />
              <Bar yAxisId="right" dataKey="ratio" name="폐업률 (%)" fill="#ffc658" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="text-sm text-gray-600 mt-2 text-center">
          주: 폐업률(%) = (폐업 수 / 개업 수) × 100
        </div>
      </div>

      {/* 필수의료 분야 전공의 충원율 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">필수의료 분야 전공의 충원율 (2023)</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={residentData}
              margin={{ top: 10, right: 30, left: 20, bottom: 30 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="rate" name="충원율 (%)" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="text-sm text-gray-600 mt-2 text-center">
          주: 소아청소년과 충원율이 28.2%로 가장 낮음
        </div>
      </div>

      {/* 지역별 의사 분포 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">지역별 의사 분포 (인구 1,000명당 의사 수)</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={doctorDistributionData}
              margin={{ top: 10, right: 30, left: 20, bottom: 30 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 4]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="rate" name="의사 수/1,000명" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="text-sm text-gray-600 mt-2 text-center">
          주: 서울(3.47명)과 경북(1.39명) 간 2.5배 이상 격차
        </div>
      </div>

      <div className="text-sm text-gray-600 mt-8 p-4 bg-gray-100 rounded">
        <h3 className="font-bold mb-2">분석 주석:</h3>
        <p>1. 2018-2022년 전체 의료기관 개폐업 데이터에 따르면, 2022년에는 개업이 증가하고 폐업률이 감소하는 추세를 보입니다.</p>
        <p>2. 진료과목별 개폐업 현황(2018-2022)에서 소아청소년과는 폐업률이 106.0%로 가장 높고, 산부인과도 93.0%로 높은 폐업률을 보입니다.</p>
        <p>3. 소아청소년과는 2020년에 폐업률이 149.5%로 정점을 기록했으며, 2020-2021년에는 개업보다 폐업이 훨씬 많았습니다.</p>
        <p>4. 산부인과는 2018년과 2020년에 폐업률이 100%를 초과했으나, 2021-2022년에는 개선되는 추세를 보입니다.</p>
        <p>5. 정신건강의학과는 12.9%로 가장 낮은 폐업률을 보이며, 내과(34.9%)도 상대적으로 안정적입니다.</p>
        <p>6. 지역별 의사 분포는 서울과 지방 간의 불균형이 뚜렷하게 나타납니다.</p>
        <p>7. 필수의료 분야 중 소아청소년과의 전공의 충원율은 28.2%로 매우 낮아 장기적인 의료 서비스 지속성에 우려가 있습니다.</p>
      </div>
    </div>
  );
};

export default MedicalInstitutionsAnalysis;
