import React from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart } from 'recharts';

const KoreanMedicalFacilityReport = () => {
  // 데이터 준비
  const yearlyStats = [
    { year: '2018', newOpen: 5889, closed: 4250, netIncrease: 1639, ratio: 72.2 },
    { year: '2019', newOpen: 5564, closed: 3883, netIncrease: 1681, ratio: 69.8 },
    { year: '2020', newOpen: 5477, closed: 3600, netIncrease: 1877, ratio: 65.7 },
    { year: '2021', newOpen: 5520, closed: 3783, netIncrease: 1737, ratio: 68.5 },
    { year: '2022', newOpen: 5756, closed: 3839, netIncrease: 1917, ratio: 66.7 }
  ];

  const typeStats = [
    { type: '의원', newOpen: 9485, closed: 5465, ratio: 57.6 },
    { type: '치과의원', newOpen: 4052, closed: 2577, ratio: 63.6 },
    { type: '한의원', newOpen: 3799, closed: 3361, ratio: 88.5 },
    { type: '약국', newOpen: 9099, closed: 6534, ratio: 71.8 },
    { type: '병원', newOpen: 527, closed: 592, ratio: 112.3 },
    { type: '요양병원', newOpen: 461, closed: 448, ratio: 97.2 },
    { type: '한방병원', newOpen: 459, closed: 225, ratio: 49.0 },
    { type: '치과병원', newOpen: 74, closed: 69, ratio: 93.2 }
  ];

  const regionalStats = [
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

  const specialtyStats = [
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
  ].sort((a, b) => b.ratio - a.ratio);

  const specialtyTrend = [
    { year: '2018', pediatrics: 122, pediatricsClosed: 121, obgyn: 45, obgynClosed: 53 },
    { year: '2019', pediatrics: 114, pediatricsClosed: 98, obgyn: 49, obgynClosed: 46 },
    { year: '2020', pediatrics: 103, pediatricsClosed: 154, obgyn: 34, obgynClosed: 41 },
    { year: '2021', pediatrics: 93, pediatricsClosed: 120, obgyn: 55, obgynClosed: 40 },
    { year: '2022', pediatrics: 87, pediatricsClosed: 57, obgyn: 60, obgynClosed: 46 }
  ];

  const recentTrend = [
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

  const regionalClinicsTrend = [
    { region: '전남', ratio: 90.3 },
    { region: '경북', ratio: 81.9 },
    { region: '충북', ratio: 77.2 },
    { region: '경남', ratio: 75.7 },
    { region: '서울', ratio: 52.8 },
    { region: '인천', ratio: 49.6 },
    { region: '경기', ratio: 45.1 }
  ];

  return (
    <div className="p-0 m-0 bg-gray-50">
      <header className="bg-blue-900 text-white p-6 text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">한국 의료기관 개폐업 현황 분석 보고서</h1>
        <p className="text-xl">지역적 불균형과 저출생의 영향, 그리고 의료체계의 구조적 문제점</p>
      </header>

      <div className="max-w-6xl mx-auto bg-white p-8 shadow-md">
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">개요</h2>
          <p className="mb-4">본 보고서는 최근 몇 년간의 한국 의료기관 개폐업 현황을 종합적으로 분석합니다. 의료기관의 개폐업 추세를 통해 한국 의료체계가 직면한 다양한 문제점들을 파악하고, 특히 지역별, 진료과목별 차이와 저출생, 의료 인프라 분포 등이 의료기관 생태계에 미치는 영향을 살펴봅니다.</p>
          
          <div className="bg-blue-50 p-4 border-l-4 border-blue-500 my-4">
            <h3 className="text-xl font-semibold text-blue-800 mb-2">주요 발견</h3>
            <ul className="list-disc pl-5 space-y-1">
              <li>수도권과 지방 간의 의료기관 개폐업 격차가 심화되고 있으며, 일부 지방에서는 폐업이 개업을 초과하는 '의료 사막화' 현상이 관찰됨</li>
              <li>저출생 현상의 영향으로 소아청소년과와 산부인과의 폐업률이 매우 높게 나타남</li>
              <li>일반 병원급 의료기관은 유일하게 폐업이 개업을 초과하는 위기 상황에 직면함</li>
              <li>정신건강의학과와 신경과는 가장 낮은 폐업률을 보이며 성장세를 유지함</li>
              <li>의료체계의 구조적 문제점(저수가, 의료자원 분배 불균형, 관치 의료 등)이 의료기관 개폐업 현황에 큰 영향을 미치고 있음</li>
            </ul>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">1. 연도별 개폐업 추이 (2018-2022)</h2>
          
          <div className="mb-6 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={yearlyStats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Bar yAxisId="left" dataKey="newOpen" name="신규 개업" fill="#4CAF50" />
                <Bar yAxisId="left" dataKey="closed" name="폐업" fill="#F44336" />
                <Line yAxisId="right" type="monotone" dataKey="ratio" name="폐업/개업 비율(%)" stroke="#2196F3" />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
          
          <p className="mb-4">2018년부터 2022년까지 전체적으로 의료기관의 개업 수는 폐업보다 지속적으로 많았습니다. 연간 개업 수는 약 5,500~5,900개 수준을 유지했으며, 폐업 수는 3,600~4,250개 사이였습니다. 폐업/개업 비율은 평균 68.6%로, 개업 대비 약 2/3 정도의 의료기관이 폐업하는 추세를 보입니다.</p>
          
          <div className="overflow-x-auto">
            <table className="min-w-full border-collapse border border-gray-300 mb-4">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border border-gray-300 p-3">연도</th>
                  <th className="border border-gray-300 p-3">신규 개업</th>
                  <th className="border border-gray-300 p-3">폐업</th>
                  <th className="border border-gray-300 p-3">순증가</th>
                  <th className="border border-gray-300 p-3">폐업/개업 비율</th>
                </tr>
              </thead>
              <tbody>
                {yearlyStats.map((stat, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="border border-gray-300 p-3">{stat.year}</td>
                    <td className="border border-gray-300 p-3">{stat.newOpen.toLocaleString()}</td>
                    <td className="border border-gray-300 p-3">{stat.closed.toLocaleString()}</td>
                    <td className="border border-gray-300 p-3 text-green-600">+{stat.netIncrease.toLocaleString()}</td>
                    <td className="border border-gray-300 p-3">{stat.ratio}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <p className="mb-4">특히 2020년에는 코로나19 팬데믹에도 불구하고 폐업률이 가장 낮은 65.7%를 기록했으며, 순증가(+1,877개)도 가장 컸습니다. 그러나 이 추세는 전국 평균이며, 지역별, 의료기관 종별로는 큰 차이가 있습니다.</p>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">2. 종별 의료기관 개폐업 현황</h2>
          
          <div className="mb-6 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={typeStats} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis type="category" dataKey="type" width={80} />
                <Tooltip />
                <Legend />
                <Bar dataKey="newOpen" name="신규 개업" fill="#4CAF50" />
                <Bar dataKey="closed" name="폐업" fill="#F44336" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <p className="mb-4">종별 개폐업 현황에서 주목할 만한 점은 다음과 같습니다:</p>
          
          <ul className="list-disc pl-5 mb-4 space-y-2">
            <li><strong>일반 병원의 위기</strong>: 병원급 의료기관 중 일반 '병원' 카테고리만 유일하게 폐업(592개)이 개업(527개)보다 많아 112.3%의 폐업률을 보였습니다. 이는 중소병원의 경영난을 보여주는 지표입니다.</li>
            <li><strong>의원급의 안정적 성장</strong>: 의원급 의료기관은 높은 개업 수와 낮은 폐업률을 보였으며, 특히 일반 의원은 57.6%의 낮은 폐업률을 기록했습니다.</li>
            <li><strong>한의원의 높은 폐업률</strong>: 한의원은 88.5%의 높은 폐업률을 보여 의원급 의료기관 중에서는 상대적으로 경영이 불안정함을 시사합니다.</li>
            <li><strong>한방병원의 성장</strong>: 한방병원은 49.0%의 가장 낮은 폐업률을 보여, 개업이 폐업의 2배 이상으로 나타났습니다.</li>
          </ul>
          
          <div className="overflow-x-auto">
            <table className="min-w-full border-collapse border border-gray-300 mb-4">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border border-gray-300 p-3">종별</th>
                  <th className="border border-gray-300 p-3">신규 개업 합계</th>
                  <th className="border border-gray-300 p-3">폐업 합계</th>
                  <th className="border border-gray-300 p-3">순증가</th>
                  <th className="border border-gray-300 p-3">폐업/개업 비율</th>
                </tr>
              </thead>
              <tbody>
                {typeStats.map((stat, index) => (
                  <tr key={index} 
                      className={stat.ratio > 100 ? 'bg-red-50' : (index % 2 === 0 ? 'bg-white' : 'bg-gray-50')}>
                    <td className="border border-gray-300 p-3">{stat.type}</td>
                    <td className="border border-gray-300 p-3">{stat.newOpen.toLocaleString()}</td>
                    <td className="border border-gray-300 p-3">{stat.closed.toLocaleString()}</td>
                    <td className={`border border-gray-300 p-3 ${(stat.newOpen - stat.closed) > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {(stat.newOpen - stat.closed) > 0 ? '+' : ''}{(stat.newOpen - stat.closed).toLocaleString()}
                    </td>
                    <td className="border border-gray-300 p-3">{stat.ratio}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="bg-blue-50 p-4 border-l-4 border-blue-500 mb-4">
            <p>병원급 의료기관 중 일반 병원만 유일하게 폐업이 개업을 초과하여 마이너스 성장을 기록했습니다. 이는 중소병원의 경영난이 매우 심각한 상태임을 보여주며, 특히 의료전달체계의 중간 단계에 위치한 일반 병원의 어려움이 큰 것으로 나타났습니다.</p>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">3. 지역별 의료기관 개폐업 현황</h2>
          
          <div className="mb-6 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regionalStats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="region" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="newOpen" name="신규 개업" fill="#4CAF50" />
                <Bar dataKey="closed" name="폐업" fill="#F44336" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <p className="mb-4">지역별 의료기관 개폐업 현황은 수도권과 지방 간 의료 격차를 명확하게 보여줍니다:</p>
          
          <ul className="list-disc pl-5 mb-4 space-y-2">
            <li><strong>수도권 집중 현상</strong>: 2018-2022년 기간 동안 경기도(+3,128개)와 서울(+2,026개)에서 가장 큰 순증가가 발생했습니다. 경기도는 57.3%, 서울은 73.1%의 폐업률을 보였습니다.</li>
            <li><strong>세종시의 급성장</strong>: 세종시는 35.9%의 매우 낮은 폐업률을 보여 인구 증가에 따른 의료기관의 급속한 성장이 있었음을 알 수 있습니다.</li>
            <li><strong>지방의 의료기관 감소 추세</strong>: 최근 2023년 자료에 따르면, 일부 지방에서는 폐업하는 의료기관이 개업하는 기관보다 많아지는 우려스러운 현상이 나타나고 있습니다.</li>
          </ul>
          
          <h3 className="text-xl font-semibold mb-2">2023년 주요 지역 폐업/개업 비율</h3>
          
          <div className="mb-6 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={recentTrend} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 120]} />
                <YAxis type="category" dataKey="region" width={60} />
                <Tooltip />
                <Legend />
                <Bar 
                  dataKey="ratio" 
                  name="폐업/개업 비율(%)" 
                  fill={(entry) => entry.ratio > 100 ? '#F44336' : (entry.ratio > 80 ? '#FFC107' : '#4CAF50')} 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="bg-blue-50 p-4 border-l-4 border-blue-500 mb-4">
            <p>2023년 전남에서는 폐업한 의료기관이 104곳으로, 신규 개업한 의료기관(94곳)보다 10곳 많았으며, 폐업률은 110.6%였습니다. 울산에서도 폐업률이 108.7%로 개업보다 많았습니다. 이는 지역 간 의료 격차가 심화되고 있으며, 일부 지방에서는 '의료 사막화' 현상이 진행 중임을 시사합니다.</p>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">4. 진료과목별 개폐업 현황</h2>
          
          <div className="mb-6 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={specialtyStats} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 120]} />
                <YAxis type="category" dataKey="specialty" width={120} />
                <Tooltip />
                <Legend />
                <Bar 
                  dataKey="ratio" 
                  name="폐업/개업 비율(%)" 
                  fill={(entry) => entry.ratio > 100 ? '#F44336' : (entry.ratio > 90 ? '#FFC107' : '#4CAF50')} 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <p className="mb-4">진료과목별 개폐업 현황에서 가장 주목할 만한 특징은 저출생 현상의 영향입니다:</p>
          
          <ul className="list-disc pl-5 mb-4 space-y-2">
            <li><strong>소아청소년과의 위기</strong>: 소아청소년과는 유일하게 폐업(550개)이 개업(519개)보다 많은 진료과목으로, 폐업/개업 비율이 106.0%에 달했습니다.</li>
            <li><strong>산부인과의 높은 폐업률</strong>: 산부인과 역시 93.0%의 높은 폐업률을 보였으며, 저출생 현상의 직접적인 영향을 받고 있습니다.</li>
            <li><strong>정신건강 분야의 성장</strong>: 정신건강의학과는 15.1%의 가장 낮은 폐업률을 보였으며, 신경과(17.5%) 역시 매우 낮은 폐업률을 기록했습니다.</li>
          </ul>
          
          <h3 className="text-xl font-semibold mb-2">소아청소년과 및 산부인과 개폐업 추이 (2018-2022)</h3>
          
          <div className="mb-6 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={specialtyTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="pediatrics" name="소아청소년과 개업" stroke="#4CAF50" />
                <Line type="monotone" dataKey="pediatricsClosed" name="소아청소년과 폐업" stroke="#F44336" strokeDasharray="5 5" />
                <Line type="monotone" dataKey="obgyn" name="산부인과 개업" stroke="#2196F3" />
                <Line type="monotone" dataKey="obgynClosed" name="산부인과 폐업" stroke="#FF9800" strokeDasharray="5 5" />
              </LineChart>
            </ResponsiveContainer>
          </div>
          
          <div className="bg-blue-50 p-4 border-l-4 border-blue-500 mb-4">
            <p>2020-2024년 기간에는 전국에서 소아청소년과 의원 426곳이 개업했지만 447곳이 폐업해 104.9%의 폐업률을 기록했습니다. 산부인과 의원은 248곳이 개업하고 219곳이 폐업해 88.3%의 폐업률을 기록했습니다. 이는 한국의 저출생 현상이 의료 생태계에 직접적인 영향을 미치고 있음을 명확하게 보여줍니다.</p>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">5. 지역별 의원 개폐업 현황</h2>
          
          <div className="mb-6 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regionalClinicsTrend} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 100]} />
                <YAxis type="category" dataKey="region" width={60} />
                <Tooltip />
                <Legend />
                <Bar 
                  dataKey="ratio" 
                  name="폐업/개업 비율(%)" 
                  fill={(entry) => entry.ratio > 80 ? '#F44336' : (entry.ratio > 60 ? '#FFC107' : '#4CAF50')} 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <p className="mb-4">의원급 의료기관(동네의원)의 지역별 개폐업 현황은 수도권과 지방의 격차를 더욱 명확하게 보여줍니다:</p>
          
          <ul className="list-disc pl-5 mb-4 space-y-2">
            <li><strong>수도권 중심의 개업 추세</strong>: 2018-2022년 기간 동안 서울과 경기에서 압도적으로 많은 의원이 개업했으며, 상대적으로 낮은 폐업률을 보였습니다.</li>
            <li><strong>지방 의원의 높은 폐업률</strong>: 전남(81.7%), 경북(79.1%), 전북(77.5%) 등 지방에서는 높은 폐업률을 보였습니다.</li>
            <li><strong>최근 5년간 지역 격차 심화</strong>: 2020-2024년 기간에는 전남의 의원 폐업률이 90.3%에 달해 거의 개업 수준으로 폐업이 일어나고 있습니다.</li>
          </ul>
          
          <div className="bg-blue-50 p-4 border-l-4 border-blue-500 mb-4">
            <p>의원급 의료기관의 지역별 개폐업 현황은 의료 접근성의 지역적 불균형을 더욱 명확하게 보여줍니다. 경기도의 폐업률은 45.1%에 그친 반면, 전남은 90.3%에 달해 거의 개업과 폐업이 동일한 수준입니다. 이러한 지역 간 격차는 '의료 사막화'라고 불리는 현상이 일부 지방에서 나타나고 있어 우려를 낳고 있습니다.</p>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">6. 의료붕괴의 구조적 원인</h2>
          
          <p className="mb-4">한국 의료체계는 단순한 의사 수 부족의 문제가 아닌 다양한 구조적 원인으로 인해 위기에 직면해 있습니다. 현재 의료기관의 개폐업 현황은 이러한 구조적 문제의 표면적 증상으로 볼 수 있습니다.</p>
          
          <div className="bg-white p-6 shadow-md rounded-md mb-6">
            <h3 className="text-xl font-semibold mb-4">주요 구조적 원인</h3>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">1. 필수의료 분야의 저수가 문제</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>한국의 의료수가는 다른 선진국에 비해 현저히 낮은 수준</li>
              <li>자연분만: 한국 54만원 vs 미국 660만원, 독일/프랑스 약 300만원</li>
              <li>맹장수술: 한국 78달러 vs 미국 584달러, 독일 178달러</li>
              <li>저수가는 의료기관의 수익성을 저하시키고, 의사들이 필수의료 분야를 기피하게 만드는 주요 원인</li>
            </ul>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">2. 의료자원의 비효율적 분배와 쏠림 현상</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>경증 환자들도 상급종합병원 선호 (2023년 기준 상급종합병원 외래 환자의 52%가 경증 환자)</li>
              <li>일차의료기관의 역할 약화와 경영난</li>
              <li>대형병원의 과밀화와 의료 질 저하</li>
              <li>의사의 과중한 업무 부담과 소진(burnout) 현상</li>
            </ul>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">3. 지역 간 의료 불균형</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>서울은 인구 1,000명당 의사 수가 3.47명인 반면, 충남은 1.53명, 경북은 1.39명에 불과</li>
              <li>의료인력의 수도권 집중 현상</li>
              <li>지방 병원의 낮은 수익성과 열악한 근무 환경</li>
              <li>특히 응급의료, 분만, 소아청소년 진료 등 필수의료 서비스의 지역 간 격차는 심각한 수준</li>
            </ul>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">4. 관치 의료와 민간의료기관 통제</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>단일 보험자인 건강보험공단을 통한 정부의 과도한 통제</li>
              <li>의료행위에 대한 과도한 규제와 통제</li>
              <li>경직된 수가 체계와 의료기관의 경영 자율성 제한</li>
              <li>관료 중심의 의사결정으로 현장 의료진의 의견 무시</li>
            </ul>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">5. 공공의료 인프라 부족</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>공공병원 비중이 전체 병원의 5~10% 수준으로 OECD 최하위 (OECD 평균 73%)</li>
              <li>의료 취약지역과 필수의료 분야의 서비스 공백</li>
              <li>의료 위기 상황 시 정부의 대응 능력 제한</li>
              <li>민간 의료기관의 수익성 중심 운영으로 인한 의료 불균형</li>
            </ul>
          </div>
        </div>
        
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">7. 해결방안</h2>
          
          <div className="bg-yellow-50 p-6 shadow-md rounded-md mb-6">
            <h3 className="text-xl font-semibold mb-4">주요 해결방안</h3>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">1. 의료수가 체계의 개선</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>필수의료 분야(응급의료, 중환자 진료, 분만, 소아청소년 진료)의 수가 현실화</li>
              <li>필수의료 분야에 대한 수가 가산제도 도입</li>
              <li>상시적 수가 조정체계 구축으로 주기적인 수가 현실화 추진</li>
              <li>의료행위별 원가분석을 통한 합리적인 수가 책정</li>
              <li>지역의료 수가 가산제도로 지역 간 의료 격차 해소 지원</li>
            </ul>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">2. 의료전달체계 개혁</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>주치의 제도 도입으로 일차의료 강화</li>
              <li>상급의료기관 이용 시 의뢰-회송 체계 강화</li>
              <li>의료기관 종별 수가 차등화로 적절한 의료이용 유도</li>
              <li>경증질환의 대형병원 이용 시 본인부담금 상향 조정</li>
            </ul>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">3. 지역의료 활성화 및 공공의료 강화</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>지역 의료기관 근무 의사에 대한 세제 혜택 및 재정적 인센티브 제공</li>
              <li>지역 의료기관의 시설 및 장비 현대화를 위한 융자 지원</li>
              <li>지역 간 의료 협력 네트워크 구축으로 의료자원 공유</li>
              <li>농어촌 의료취약지 의사에 대한 특별 수가 가산제 도입</li>
              <li>공공의료 인프라 확충과 민간-공공 협력 강화</li>
            </ul>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">4. 의료인력 양성 및 관리 방안</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>의대 교육과정에서 필수의료와 공공의료에 대한 교육 강화</li>
              <li>전공의 수련환경 개선을 통한 양질의 전문의 양성</li>
              <li>필수의료 및 지역의료 분야 종사자에 대한 인센티브 제공</li>
              <li>의사 근무환경 개선을 통한 소진 방지 및 직업 만족도 제고</li>
              <li>의사의 전문성과 자율성을 존중하는 의료 환경 조성</li>
            </ul>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">5. 의료사고 책임 분담 시스템 구축</h4>
            <ul className="list-disc pl-5 mb-4 space-y-1">
              <li>무과실 의료사고 보상제도 도입</li>
              <li>의료사고 보상기금 설립 및 운영</li>
              <li>의료분쟁 조정제도 개선 및 활성화</li>
              <li>의료소송 전문 재판부 설치 및 전문성 강화</li>
            </ul>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-blue-800 border-b-2 border-blue-400 pb-2 mb-4">결론 및 시사점</h2>
          
          <div className="bg-green-50 p-6 shadow-md rounded-md mb-6">
            <h3 className="text-xl font-semibold mb-4">주요 시사점</h3>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">1. 수도권-지방 격차 심화</h4>
            <p className="mb-2">의료기관의 개설과 유지가 수도권에 집중되고 있으며, 일부 지방에서는 폐업이 개업을 초과하는 '의료 사막화' 현상이 발생하고 있습니다. 이는 지역 간 의료 접근성 불균형을 심화시키는 요인이 됩니다.</p>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">2. 저출생의 명확한 영향</h4>
            <p className="mb-2">소아청소년과는 유일하게 폐업이 개업을 초과하는 진료과목(폐업률 106.0%)이며, 산부인과 역시 높은 폐업률(93.0%)을 보이고 있습니다. 이는 인구구조 변화가 의료기관 생태계에 직접적인 영향을 미치고 있음을 보여줍니다.</p>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">3. 의료기관 종별 양극화</h4>
            <p className="mb-2">일반 병원은 유일하게 폐업이 개업을 초과(폐업률 112.3%)하고 있으며, 요양병원과 치과병원도 높은 폐업률을 보이고 있습니다. 반면 의원과 한방병원은 상대적으로 안정적인 성장세를 유지하고 있어 의료기관 종별 양극화 현상이 나타나고 있습니다.</p>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">4. 정신건강 분야의 확장</h4>
            <p className="mb-2">정신건강의학과(15.1%)와 신경과(17.5%)는 가장 낮은 폐업률을 보이며 성장세를 유지하고 있습니다. 이는 정신건강에 대한 사회적 관심 증가를 반영하고 있습니다.</p>
            
            <h4 className="text-lg font-semibold text-blue-700 mt-4 mb-2">5. 의료체계의 구조적 문제 노출</h4>
            <p className="mb-2">의료기관 개폐업 현황은 한국 의료체계의 구조적 문제점(저수가, 의료자원 분배 불균형, 관치 의료, 공공의료 인프라 부족 등)이 현실적으로 표출된 결과입니다. 이러한 구조적 문제 해결 없이는 의료체계의 지속가능성을 확보하기 어렵습니다.</p>
            
            <h3 className="text-xl font-semibold mt-6 mb-2">종합적 결론</h3>
            <p className="mb-2">한국 의료체계의 회복과 지속가능성 확보를 위해서는 단편적인 접근이 아닌 의료체계의 근본적인 패러다임 전환이 필요합니다. 필수의료 분야의 수가 현실화, 의료전달체계 개혁, 지역 의료 활성화, 공공의료 강화 등 종합적인 대책이 필요합니다.</p>
            
            <p>특히 정부, 의료계, 시민사회 간의 진정한 소통과 협력이 필요하며, 정부는 의료계의 전문성과 현장의 목소리를 존중하는 태도를 가져야 합니다. 현재의 의료붕괴 위기를 한국 의료체계의 패러다임을 전환하고 근본적으로 개혁하는 계기로 삼아야 할 것입니다.</p>
          </div>
        </div>
        
        <footer className="text-center text-gray-600 text-sm mt-12 pt-6 border-t border-gray-200">
          <p>본 보고서는 2018-2023년 건강보험심사평가원 요양기관 개폐업 현황 데이터 및 관련 연구자료를 기반으로 작성되었습니다.</p>
          <p className="mt-2">작성일: 2025년 5월 18일</p>
        </footer>
      </div>
    </div>
  );
};

export default KoreanMedicalFacilityReport;
