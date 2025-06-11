import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, ComposedChart } from 'recharts';

const YearlyStats = [
  { year: '2018', newOpen: 5889, closed: 4250, netIncrease: 1639, ratio: 72.2 },
  { year: '2019', newOpen: 5564, closed: 3883, netIncrease: 1681, ratio: 69.8 },
  { year: '2020', newOpen: 5477, closed: 3600, netIncrease: 1877, ratio: 65.7 },
  { year: '2021', newOpen: 5520, closed: 3783, netIncrease: 1737, ratio: 68.5 },
  { year: '2022', newOpen: 5756, closed: 3839, netIncrease: 1917, ratio: 66.7 }
];

const RegionalStats = [
  { region: '서울', newOpen: 7518, closed: 5492, netIncrease: 2026, ratio: 73.1 },
  { region: '경기', newOpen: 7329, closed: 4201, netIncrease: 3128, ratio: 57.3 },
  { region: '인천', newOpen: 1443, closed: 903, netIncrease: 540, ratio: 62.6 },
  { region: '부산', newOpen: 2015, closed: 1446, netIncrease: 569, ratio: 71.8 },
  { region: '대구', newOpen: 1254, closed: 843, netIncrease: 411, ratio: 67.2 },
  { region: '광주', newOpen: 869, closed: 652, netIncrease: 217, ratio: 75.0 },
  { region: '대전', newOpen: 750, closed: 586, netIncrease: 164, ratio: 78.1 },
  { region: '울산', newOpen: 383, closed: 310, netIncrease: 73, ratio: 80.9 },
  { region: '세종', newOpen: 245, closed: 88, netIncrease: 157, ratio: 35.9 },
  { region: '경남', newOpen: 1309, closed: 978, netIncrease: 331, ratio: 74.7 }
];

const TypeStats = [
  { type: '의원', newOpen: 9485, closed: 5465, ratio: 57.6 },
  { type: '치과의원', newOpen: 4052, closed: 2577, ratio: 63.6 },
  { type: '한의원', newOpen: 3799, closed: 3361, ratio: 88.5 },
  { type: '약국', newOpen: 9099, closed: 6534, ratio: 71.8 },
  { type: '병원', newOpen: 527, closed: 592, ratio: 112.3 },
  { type: '요양병원', newOpen: 461, closed: 448, ratio: 97.2 },
  { type: '한방병원', newOpen: 459, closed: 225, ratio: 49.0 },
  { type: '치과병원', newOpen: 74, closed: 69, ratio: 93.2 }
];

const SpecialtyStats = [
  { specialty: '정신건강의학과', ratio: 15.1 },
  { specialty: '신경과', ratio: 17.5 },
  { specialty: '내과', ratio: 34.9 },
  { specialty: '정형외과', ratio: 39.6 },
  { specialty: '피부과', ratio: 41.9 },
  { specialty: '이비인후과', ratio: 56.8 },
  { specialty: '안과', ratio: 61.2 },
  { specialty: '가정의학과', ratio: 67.3 },
  { specialty: '일반의', ratio: 74.0 },
  { specialty: '외과', ratio: 76.8 },
  { specialty: '산부인과', ratio: 93.0 },
  { specialty: '소아청소년과', ratio: 106.0 }
];

// Special data for children and obgyn over 5 years
const SpecialtyTrend = [
  { year: '2018', pediatrics: 122, pediatricsClosed: 121, obgyn: 45, obgynClosed: 53 },
  { year: '2019', pediatrics: 114, pediatricsClosed: 98, obgyn: 49, obgynClosed: 46 },
  { year: '2020', pediatrics: 103, pediatricsClosed: 154, obgyn: 34, obgynClosed: 41 },
  { year: '2021', pediatrics: 93, pediatricsClosed: 120, obgyn: 55, obgynClosed: 40 },
  { year: '2022', pediatrics: 87, pediatricsClosed: 57, obgyn: 60, obgynClosed: 46 }
];

// Regional clinics only
const RegionalClinics = [
  { region: '서울', newOpen: 3017, closed: 1705, ratio: 56.5 },
  { region: '경기', newOpen: 2315, closed: 1081, ratio: 46.7 },
  { region: '인천', newOpen: 482, closed: 258, ratio: 53.5 },
  { region: '부산', newOpen: 709, closed: 426, ratio: 60.1 },
  { region: '대구', newOpen: 433, closed: 228, ratio: 52.7 },
  { region: '경남', newOpen: 356, closed: 249, ratio: 69.9 },
  { region: '경북', newOpen: 263, closed: 208, ratio: 79.1 },
  { region: '광주', newOpen: 284, closed: 177, ratio: 62.3 },
  { region: '전남', newOpen: 202, closed: 165, ratio: 81.7 },
  { region: '전북', newOpen: 236, closed: 183, ratio: 77.5 }
];

// Recent trend by region showing some areas with negative growth
const RecentTrend = [
  { region: '전남', ratio: 110.6, description: '폐업 > 개업' },
  { region: '울산', ratio: 108.7, description: '폐업 > 개업' },
  { region: '충북', ratio: 97.6, description: '거의 균형' },
  { region: '경남', ratio: 89.2, description: '소폭 증가' },
  { region: '전북', ratio: 88.5, description: '소폭 증가' },
  { region: '광주', ratio: 83.6, description: '소폭 증가' },
  { region: '서울', ratio: 68.3, description: '성장세' },
  { region: '경기', ratio: 65.3, description: '성장세' },
  { region: '인천', ratio: 60.8, description: '강한 성장세' }
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];
const RED_COLOR = '#FF6B6B';
const GREEN_COLOR = '#4CAF50';

const HealthcareFacilityCharts = () => {
  return (
    <div className="p-4 bg-white">
      <h1 className="text-2xl font-bold text-center mb-8">한국 요양기관 개폐업 현황 그래프 분석 (2018-2022)</h1>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">1. 연도별 요양기관 개폐업 추이</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={YearlyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="newOpen" name="신규 개업" fill="#4CAF50" />
              <Bar yAxisId="left" dataKey="closed" name="폐업" fill="#FF6B6B" />
              <Line yAxisId="right" type="monotone" dataKey="ratio" name="폐업/개업 비율(%)" stroke="#8884d8" />
            </ComposedChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">2018년부터 2022년까지 개업 수는 폐업 수보다 지속적으로 높았으며, 폐업/개업 비율은 65.7%~72.2% 사이를 유지</p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">2. 종별 요양기관 개폐업 현황</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={TypeStats} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="type" width={80} />
              <Tooltip />
              <Legend />
              <Bar dataKey="newOpen" name="신규 개업" fill="#4CAF50" />
              <Bar dataKey="closed" name="폐업" fill="#FF6B6B" />
            </BarChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">일반 '병원' 카테고리만 폐업이 개업보다 많음, 의원과 약국은 높은 개업 수를 유지</p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">3. 진료과목별 폐업/개업 비율</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={SpecialtyStats} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 120]} />
              <YAxis type="category" dataKey="specialty" width={120} />
              <Tooltip />
              <Legend />
              <Bar dataKey="ratio" name="폐업/개업 비율(%)" fill={(entry) => entry.ratio > 100 ? RED_COLOR : (entry.ratio > 90 ? '#FFBB28' : '#4CAF50')} />
            </BarChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">소아청소년과는 유일하게 폐업/개업 비율이 100%를 초과, 정신건강의학과와 신경과는 가장 낮은 폐업률</p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">4. 소아청소년과 및 산부인과 개폐업 추이</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={SpecialtyTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="pediatrics" name="소아청소년과 개업" stroke="#4CAF50" />
              <Line type="monotone" dataKey="pediatricsClosed" name="소아청소년과 폐업" stroke="#FF6B6B" strokeDasharray="5 5" />
              <Line type="monotone" dataKey="obgyn" name="산부인과 개업" stroke="#0088FE" />
              <Line type="monotone" dataKey="obgynClosed" name="산부인과 폐업" stroke="#FF8042" strokeDasharray="5 5" />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">저출생 영향으로 소아청소년과와 산부인과의 폐업 추세가 뚜렷함</p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">5. 지역별 요양기관 개폐업 현황 (상위 10개 지역)</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={RegionalStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="newOpen" name="신규 개업" fill="#4CAF50" />
              <Bar dataKey="closed" name="폐업" fill="#FF6B6B" />
            </BarChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">서울과 경기 지역의 개업 수가 압도적으로 많으며, 순증가도 가장 높음</p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">6. 지역별 폐업/개업 비율</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={RegionalStats} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="region" width={50} />
              <Tooltip />
              <Legend />
              <Bar dataKey="ratio" name="폐업/개업 비율(%)" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">세종은 가장 낮은 폐업률(35.9%)을, 경북, 울산, 충남은 높은 폐업률을 보임</p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">7. 의원급 의료기관 지역별 폐업/개업 비율</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={RegionalClinics} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="region" width={50} />
              <Tooltip />
              <Legend />
              <Bar dataKey="ratio" name="폐업/개업 비율(%)" fill={(entry) => entry.ratio > 80 ? '#FFBB28' : (entry.ratio > 70 ? '#00C49F' : '#4CAF50')} />
            </BarChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">의원급 의료기관에서도 지역별 격차가 뚜렷함. 전남과 경북, 전북은 높은 폐업률을 보임</p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">8. 2023년 주요 지역 폐업/개업 비율 현황</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={RecentTrend} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 120]} />
              <YAxis type="category" dataKey="region" width={50} />
              <Tooltip />
              <Legend />
              <Bar dataKey="ratio" name="폐업/개업 비율(%)" fill={(entry) => entry.ratio > 100 ? RED_COLOR : (entry.ratio > 80 ? '#FFBB28' : '#4CAF50')} />
            </BarChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">2023년 일부 지역(전남, 울산)에서는 폐업이 개업을 초과, 지역 간 의료 격차가 심화됨</p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">9. 종별 요양기관 폐업/개업 비율 분포</h2>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={TypeStats}
                cx="50%"
                cy="50%"
                labelLine={true}
                outerRadius={120}
                fill="#8884d8"
                dataKey="ratio"
                nameKey="type"
                label={({name, percent}) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {TypeStats.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.ratio > 100 ? RED_COLOR : COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value.toFixed(1)}%`, '폐업/개업 비율']} />
            </PieChart>
          </ResponsiveContainer>
          <p className="text-sm text-center mt-2 text-gray-600">병원, 치과병원, 한의원은 상대적으로 높은 폐업률을 보임</p>
        </div>
      </div>
    </div>
  );
};

export default HealthcareFacilityCharts;