import React, { useState } from 'react';
import { 
  LineChart, Line, BarChart, Bar, 
  XAxis, YAxis, CartesianGrid, Tooltip, 
  Legend, ResponsiveContainer, ComposedChart,
  Area, ReferenceLine, Cell
} from 'recharts';

const HealthInsuranceReport = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // 재정 추이 데이터
  const financialData = [
    { year: '2009', income: 31.5, expense: 31.2, balance: 0.3 },
    { year: '2010', income: 33.9, expense: 34.9, balance: -1.0 },
    { year: '2011', income: 38.8, expense: 37.3, balance: 1.5 },
    { year: '2012', income: 42.5, expense: 39.2, balance: 3.3 },
    { year: '2013', income: 47.2, expense: 41.3, balance: 5.9 },
    { year: '2014', income: 50.5, expense: 44.8, balance: 5.8 },
    { year: '2015', income: 53.3, expense: 48.2, balance: 5.1 },
    { year: '2016', income: 56.5, expense: 53.7, balance: 2.7 },
    { year: '2017', income: 58.8, expense: 58.0, balance: 0.8 },
    { year: '2018', income: 62.7, expense: 66.0, balance: -3.3 },
    { year: '2019', income: 69.2, expense: 72.1, balance: -2.9 },
    { year: '2020', income: 75.1, expense: 73.6, balance: 1.5 },
    { year: '2021', income: 81.7, expense: 79.0, balance: 2.8 },
    { year: '2022', income: 91.0, expense: 86.2, balance: 4.8 },
    { year: '2023', income: 96.4, expense: 94.7, balance: 1.7 }
  ];

  // 재정 누적 데이터
  const cumulativeData = [
    { year: '2014', surplus: 15.9, reserve: 12.8, difference: -3.1 },
    { year: '2015', surplus: 21.0, reserve: 17.0, difference: -4.0 },
    { year: '2016', surplus: 23.7, reserve: 20.1, difference: -3.6 },
    { year: '2017', surplus: 24.5, reserve: 20.8, difference: -3.7 },
    { year: '2018', surplus: 21.2, reserve: 20.6, difference: -0.6 },
    { year: '2019', surplus: 18.3, reserve: 17.8, difference: -0.5 },
    { year: '2020', surplus: 19.8, reserve: 17.4, difference: -2.4 },
    { year: '2021', surplus: 22.6, reserve: 20.2, difference: -2.4 },
    { year: '2022', surplus: 27.4, reserve: 23.9, difference: -3.5 },
    { year: '2023', surplus: 29.1, reserve: 28.0, difference: -1.1 }
  ];

  // 보장률 데이터
  const coverageData = [
    { year: '2017', overall: 62.7, major: 80.1 },
    { year: '2018', overall: 63.8, major: 80.5 },
    { year: '2019', overall: 64.2, major: 80.8 },
    { year: '2020', overall: 65.3, major: 81.0 },
    { year: '2021', overall: 65.6, major: 81.2 },
    { year: '2022', overall: 65.7, major: 81.5 },
    { year: '2023', overall: 64.9, major: 81.8 }
  ];

  // 적립률 데이터
  const allocationRateData = [
    { year: '2015', profit: 5.13, reserve: 4.17, rate: 81.3 },
    { year: '2016', profit: 2.72, reserve: 3.09, rate: 113.6 },
    { year: '2017', profit: 0.80, reserve: 0.71, rate: 88.8 },
    { year: '2018', profit: -3.26, reserve: -0.17, rate: 5.2 },
    { year: '2019', profit: -2.92, reserve: -2.82, rate: 96.6 },
    { year: '2020', profit: 1.50, reserve: -0.35, rate: -23.3 },
    { year: '2021', profit: 2.76, reserve: 2.82, rate: 102.2 },
    { year: '2022', profit: 4.83, reserve: 3.63, rate: 75.2 },
    { year: '2023', profit: 1.69, reserve: 4.13, rate: 244.4 }
  ];

  // 민간보험 데이터
  const privateInsuranceData = [
    { year: '2021', nonCovered: 7.9, covered: 4.6 },
    { year: '2022', nonCovered: 7.95, covered: 5.4 },
    { year: '2023', nonCovered: 8.0, covered: 6.1 }
  ];

  // 필수의료 수익성 추이 데이터
  const essentialMedicalData = [
    { year: '2018', surgery: 100, emergency: 100, critical: 100 },
    { year: '2019', surgery: 98, emergency: 95, critical: 97 },
    { year: '2020', surgery: 95, emergency: 90, critical: 93 },
    { year: '2021', surgery: 90, emergency: 85, critical: 89 },
    { year: '2022', surgery: 85, emergency: 80, critical: 85 },
    { year: '2023', surgery: 80, emergency: 75, critical: 81 }
  ];

  // 의료인력 데이터
  const medicalWorkforceData = [
    { category: '흉부외과', current: 196, retiring: 196, newDoctors: 12 },
    { category: '산부인과', current: 540, retiring: 220, newDoctors: 80 },
    { category: '응급의학과', current: 380, retiring: 95, newDoctors: 62 },
    { category: '소아과', current: 720, retiring: 280, newDoctors: 130 }
  ];

  // 재정 테이블 데이터
  const financeTableData = [
    { year: '2018', profit: -3.26, accumulated: 21.24, reserve: 20.60, diff: -0.65, diffPercent: -3.05 },
    { year: '2019', profit: -2.92, accumulated: 18.32, reserve: 17.77, diff: -0.55, diffPercent: -2.99 },
    { year: '2020', profit: 1.50, accumulated: 19.82, reserve: 17.42, diff: -2.40, diffPercent: -12.10 },
    { year: '2021', profit: 2.76, accumulated: 22.57, reserve: 20.24, diff: -2.33, diffPercent: -10.33 },
    { year: '2022', profit: 4.83, accumulated: 27.40, reserve: 23.87, diff: -3.53, diffPercent: -12.90 },
    { year: '2023', profit: 1.69, accumulated: 29.09, reserve: 28.00, diff: -1.09, diffPercent: -3.76 }
  ];

  const formatNumber = (num) => {
    return Number(num).toFixed(2);
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="max-w-6xl mx-auto p-4 bg-gray-50">
      <h1 className="text-3xl font-bold text-center mb-6 pb-3 border-b-2 border-blue-500 text-gray-800">건강보험의 재정현황과 문제점</h1>
      
      <div className="author-info text-center mb-8">
        <p className="text-gray-600">작성일: 2025년 5월 18일</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow mb-8">
        <h2 className="text-xl font-bold mb-3 text-gray-800">초록</h2>
        <p className="bg-gray-50 p-4 border-l-4 border-blue-500 italic">
          본 논문은 한국 건강보험제도의 재정 현황과 구조적 문제점을 분석한다. 특히 최근 4년간 지속된 건강보험 재정 흑자와 30조원에 이르는 적립금에도 불구하고 필수의료 서비스 붕괴, 보장률 조작 논란, 독과점으로 인한 비효율성 등 제도의 심각한 구조적 문제를 검토한다. 건강보험 재정의 불균형한 관리, 투명성 부족, 당기순이익과 법정준비금 간 불일치, 그리고 이러한 문제가 야기하는 의료 시스템의 지속가능성 위기를 면밀히 분석한다. 본 연구는 건강보험 재정 운영의 개선방안과 의료시스템의 지속가능한 발전을 위한 정책적 제언을 제시한다.
        </p>
      </div>

      <div className="flex mb-6 border-b">
        <button 
          className={`px-4 py-2 ${activeTab === 'overview' ? 'text-blue-600 border-b-2 border-blue-600 font-medium' : 'text-gray-600'}`}
          onClick={() => handleTabChange('overview')}>
          재정 현황
        </button>
        <button 
          className={`px-4 py-2 ${activeTab === 'problems' ? 'text-blue-600 border-b-2 border-blue-600 font-medium' : 'text-gray-600'}`}
          onClick={() => handleTabChange('problems')}>
          주요 문제점
        </button>
        <button 
          className={`px-4 py-2 ${activeTab === 'solutions' ? 'text-blue-600 border-b-2 border-blue-600 font-medium' : 'text-gray-600'}`}
          onClick={() => handleTabChange('solutions')}>
          정책 제언
        </button>
      </div>
      
      {activeTab === 'overview' && (
        <div>
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <h2 className="text-xl font-bold mb-3 text-gray-800">I. 서론</h2>
            <p className="mb-4">
              한국의 건강보험제도는 전국민을 대상으로 하는 단일보험자 방식의 사회보험으로, 1989년 전국민 의료보험 시행 이후 의료 접근성 향상과 국민 건강 증진에 기여해왔다. 그러나 최근 건강보험 재정 운영의 불투명성, 과도한 적립금 축적, 필수의료 서비스 붕괴 등 다양한 문제점이 지적되면서 제도의 근본적인 개혁 필요성이 제기되고 있다.
            </p>
            <p>
              흑자 재정에도 불구하고 의료 시스템의 지속가능성이 위협받는 역설적인 상황은 건강보험 재정 운영의 구조적 문제와 깊은 관련이 있다. 본 논문은 건강보험 재정의 현황을 분석하고, 제도가 당면한 주요 문제점을 식별하며, 이를 바탕으로 개선방안을 모색하고자 한다.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <h2 className="text-xl font-bold mb-3 text-gray-800">II. 건강보험 재정 현황</h2>
            
            <h3 className="text-lg font-semibold mb-3 mt-6 text-gray-700">2.1 재정 추이 분석</h3>
            
            <div className="mb-6 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={financialData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`${value.toFixed(1)} 조원`]} />
                  <Legend />
                  <Bar dataKey="income" name="수입" fill="#8884d8" />
                  <Bar dataKey="expense" name="지출" fill="#82ca9d" />
                  <Line type="monotone" dataKey="balance" name="당기수지차" stroke="#ff7300" strokeWidth={2} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
            
            <p className="mb-4">
              한국 건강보험 재정은 2020년부터 4년 연속 흑자를 기록하고 있다. 2023년 기준 당기수지 흑자는 1조 6,864억원이며, 누적 적립금은 29조 7,221억원에 달한다. 특히 주목할 점은 2023년, 2024년, 2025년에 의료보험료가 인상되지 않았음에도 불구하고 건강보험공단은 흑자를 지속하고 있다는 것이다.
            </p>

            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
              <p><strong>주목할 점:</strong> 건강보험공단의 당기순이익과 누적 법정준비금 간에는 상당한 불일치가 존재한다. 2023년 기준으로 누적 당기순이익(29.09조원)과 누적 법정준비금(28.00조원) 간에는 1.09조원의 차이가 있으며, 이 차이는 연도별로 큰 변동을 보인다.</p>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr>
                    <th>연도</th>
                    <th>당기순이익(조원)</th>
                    <th>누적당기순이익(조원)</th>
                    <th>누적법정준비금(조원)</th>
                    <th>차이(조원)</th>
                    <th>차이(%)</th>
                  </tr>
                </thead>
                <tbody>
                  {financeTableData.map((row, index) => (
                    <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
                      <td>{row.year}</td>
                      <td className={row.profit >= 0 ? 'text-green-600' : 'text-red-600'}>
                        {formatNumber(row.profit)}
                      </td>
                      <td>{formatNumber(row.accumulated)}</td>
                      <td>{formatNumber(row.reserve)}</td>
                      <td className={row.diff >= 0 ? 'text-green-600' : 'text-red-600'}>
                        {formatNumber(row.diff)}
                      </td>
                      <td className={row.diffPercent >= 0 ? 'text-green-600' : 'text-red-600'}>
                        {formatNumber(row.diffPercent)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="text-sm text-gray-500 mt-2">자료출처: 건강보험공단 재정현황 데이터 분석</p>

            <h3 className="text-lg font-semibold mb-3 mt-6 text-gray-700">2.2 누적 당기순이익과 법정준비금 비교</h3>
            
            <div className="mb-6 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={cumulativeData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`${value.toFixed(1)} 조원`]} />
                  <Legend />
                  <Line type="monotone" dataKey="surplus" name="누적 당기순이익" stroke="#8884d8" strokeWidth={2} />
                  <Line type="monotone" dataKey="reserve" name="누적 법정준비금" stroke="#82ca9d" strokeWidth={2} />
                  <Line type="monotone" dataKey="difference" name="차이" stroke="#ff7300" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            <p className="mb-4">
              건강보험 재정은 2018년과 2019년 일시적인 적자를 기록했으나, 2020년부터 다시 흑자로 전환되었다. 2023년 현재 누적 당기순이익과 누적 법정준비금 간의 차이는 2020-2022년에 비해 감소했으나, 여전히 1조원 이상의 불일치가 있다. 특히 2020년에는 당기순이익이 양수임에도 불구하고 법정준비금이 오히려 감소하는 이례적인 현상이 발생했다.
            </p>

            <h3 className="text-lg font-semibold mb-3 mt-6 text-gray-700">2.3 보장률 현황과 문제점</h3>
            
            <div className="mb-6 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={coverageData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis domain={[50, 90]} />
                  <Tooltip formatter={(value) => [`${value.toFixed(1)}%`]} />
                  <Legend />
                  <Bar dataKey="overall" name="전체 보장률" fill="#8884d8" />
                  <Line type="monotone" dataKey="major" name="4대 중증질환 보장률" stroke="#ff7300" strokeWidth={2} />
                  <ReferenceLine y={70} stroke="red" strokeDasharray="3 3" label={{ value: '목표 보장률 70%', position: 'right' }} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
            
            <p className="mb-4">
              2023년 건강보험 보장률은 전년보다 0.8%p 하락한 64.9%로 나타났다. 반면 4대 중증질환 보장률은 81.8%로 전년(81.5%) 대비 0.3%p 상승했다. 2017년 문재인 케어 시행 이후 보장률은 총 2%p 정도 상승했으나, 당초 목표했던 70%에는 여전히 크게 못 미치는 상황이다.
            </p>
          </div>
        </div>
      )}

      {activeTab === 'problems' && (
        <div>
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <h2 className="text-xl font-bold mb-3 text-gray-800">III. 건강보험 재정의 주요 문제점</h2>
            
            <h3 className="text-lg font-semibold mb-3 mt-6 text-gray-700">3.1 재정 운영의 불규칙성과 투명성 부족</h3>
            
            <div className="mb-6 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={allocationRateData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis domain={[-50, 250]} />
                  <Tooltip formatter={(value, name) => [
                    name === 'rate' ? `${value.toFixed(1)}%` : `${value.toFixed(2)} 조원`,
                    name === 'rate' ? '적립률' : (name === 'profit' ? '당기순이익' : '법정준비금 증가액')
                  ]} />
                  <Legend />
                  <Bar dataKey="profit" name="당기순이익" fill="#8884d8" />
                  <Bar dataKey="reserve" name="법정준비금 증가액" fill="#82ca9d" />
                  <Line type="monotone" dataKey="rate" name="적립률(%)" stroke="#ff7300" strokeWidth={2} />
                  <ReferenceLine y={100} stroke="red" strokeDasharray="3 3" label={{ value: '적정 적립률 100%', position: 'right' }} />
                  <ReferenceLine y={0} stroke="black" />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
            
            <p className="mb-4">
              건강보험 재정 운영에 있어 가장 심각한 문제 중 하나는 당기순이익에 대한 법정준비금 적립률의 불규칙성이다. 분석 결과, 적립률은 -23.60%에서 244.76%까지 연도별로 크게 달라지며 일관된 규칙이 없다. 이는 건강보험 재정이 규정대로 처리되지 않을 가능성을 시사한다.
            </p>
            
            <p className="mb-4">
              특히 주목할 점은 2020년의 경우 당기순이익이 1.50조원 발생했음에도 법정준비금은 오히려 0.35조원 감소하는 이례적인 상황이 발생했다는 것이다. 또한 2014-2017년에는 누적 당기순이익의 15-19%가 법정준비금으로 적립되지 않았다.
            </p>
            
            <p className="mb-4">
              이러한 불규칙적인 적립 패턴은 건강보험 재정 운영의 투명성 문제를 제기한다. 적립되지 않은 자금의 사용처에 대한 명확한 정보가 없어 국민의 건강보험료로 조성된 자금이 어떻게 관리되고 사용되는지에 대한 의문이 제기된다.
            </p>

            <h3 className="text-lg font-semibold mb-3 mt-6 text-gray-700">3.2 건강보험 독과점으로 인한 문제</h3>
            
            <p className="mb-4">
              한국의 건강보험제도는 전국민과 모든 의료기관의 강제 가입을 원칙으로 하는 단일보험자 방식으로 운영되고 있다. 이러한 독과점 구조는 다음과 같은 문제를 야기한다:
            </p>
            
            <ol className="list-decimal pl-5 mb-4 space-y-2">
              <li><strong>비효율적 재정 운영:</strong> 경쟁이 없는 상황에서 건강보험공단은 방만한 경영에도 견제를 받지 않으며, 과도한 이익을 축적하고 있다.</li>
              <li><strong>의료수가의 통제:</strong> 건강보험공단은 독점적 지위를 이용하여 의료수가를 저수가로 통제하며, 이는 필수의료 서비스의 지속가능성을 위협한다.</li>
              <li><strong>비보험 진료에 대한 부당한 개입:</strong> 건강보험공단이 공적 보장 외 항목인 비보험 진료에 개입하여 통제함으로써 의료서비스의 발전과 다양성을 저해한다.</li>
            </ol>

            <h3 className="text-lg font-semibold mb-3 mt-6 text-gray-700">3.3 필수의료 수익성 저하와 의료인력 부족</h3>
            
            <div className="flex flex-wrap -mx-2">
              <div className="w-full lg:w-1/2 px-2 mb-4">
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={essentialMedicalData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis domain={[70, 105]} />
                      <Tooltip formatter={(value) => [`${value} (2018=100)`]} />
                      <Legend />
                      <Line type="monotone" dataKey="surgery" name="수술 분야" stroke="#8884d8" strokeWidth={2} />
                      <Line type="monotone" dataKey="emergency" name="응급 분야" stroke="#82ca9d" strokeWidth={2} />
                      <Line type="monotone" dataKey="critical" name="중환자 분야" stroke="#ff7300" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-sm text-center text-gray-500 mt-2">필수의료 분야 수익성 추이 (2018=100)</p>
              </div>
              
              <div className="w-full lg:w-1/2 px-2 mb-4">
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={medicalWorkforceData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="category" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`${value}명`]} />
                      <Legend />
                      <Bar dataKey="current" name="현재 전문의 수" fill="#8884d8" />
                      <Bar dataKey="retiring" name="4년내 은퇴 예정" fill="#82ca9d" />
                      <Bar dataKey="newDoctors" name="4년내 신규 배출" fill="#ff7300" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-sm text-center text-gray-500 mt-2">필수의료 인력 현황 및 전망</p>
              </div>
            </div>
            
            <p className="mb-4">
              저수가 정책과 의료인력 부족으로 인한 필수의료 붕괴 위험이 심화되고 있다. 2025년 이후 4년간 배출될 흉부외과 의사는 최대 12명에 불과한 반면, 같은 기간 은퇴하는 흉부외과 전문의는 196명에 달한다. 산부인과 전문의의 평균 연령은 이미 54.4세에 도달했다.
            </p>
            
            <p className="mb-4">
              필수의료 분야의 수익성은 2018년 이후 지속적으로 하락하고 있다. 수술 분야는 20%, 응급 분야는 25%, 중환자 분야는 19% 감소하였다. 의료보험공단이 매년 흑자를 내는 동안 의사들, 특히 필수의료 분야의 의사들은 경영난에 시달리고 있다. 이는 장기적으로 의료 접근성 감소와 의료 품질 저하로 이어질 수 있는 심각한 문제이다.
            </p>

            <h3 className="text-lg font-semibold mb-3 mt-6 text-gray-700">3.4 보장률 조작 논란</h3>
            
            <div className="bg-gray-50 p-4 my-4 text-center">
              <p className="font-bold">보장률 = 급여 / (급여 + 비급여 + 비보험) × 100%</p>
              <p className="text-sm text-gray-500">* 단, 미용성형 관련 비보험 진료와 필요시 특정 비보험진료는 제외함</p>
            </div>
            
            <p className="mb-4">
              이 계산식의 주요 문제점은 다음과 같다:
            </p>
            
            <ol className="list-decimal pl-5 mb-4 space-y-2">
              <li><strong>비보험 진료 포함:</strong> 건강보험이 보장할 필요도, 의무도 없는 비보험 진료를 계산식에 포함시켜 보장률을 인위적으로 낮게 산출한다.</li>
              <li><strong>표본조사의 제한성:</strong> 보장률은 전수조사가 아닌 표본조사(전체 요양기관의 약 2.5%)로 산출되지만, 정부는 표준오차나 신뢰구간을 공개하지 않고 마치 정확한 수치인 것처럼 제시한다.</li>
              <li><strong>자의적 포함/제외 항목:</strong> 특정 비보험 항목(예: 다초점 렌즈, 도수치료)을 포함하거나 제외함으로써 보장률을 임의로 조작할 수 있다.</li>
            </ol>

            <h3 className="text-lg font-semibold mb-3 mt-6 text-gray-700">3.5 문재인 케어와 실손보험의 구조적 문제</h3>
            
            <div className="mb-6 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={privateInsuranceData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`${value.toFixed(1)} 조원`]} />
                  <Legend />
                  <Bar dataKey="nonCovered" name="비급여 보험금" stackId="a" fill="#8884d8" />
                  <Bar dataKey="covered" name="급여 본인부담금" stackId="a" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            
            <p className="mb-4">
              2017년 시행된 문재인 케어는 의사의 비급여 진료 수익을 감소시키고, 국민 의료비 부담을 실손보험으로 전가하는 결과를 가져왔다. 2021년부터 2023년까지 실손보험의 비급여 보험금은 7.9조원에서 8조원으로 0.1조원(1.8%) 증가한 반면, 건강보험 본인부담금은 4.6조원에서 6.1조원으로 1.5조원(32.5%) 증가했다.
            </p>
            
            <p className="mb-4">
              실손보험은 점차 '제2의 건강보험공단'으로 기능하면서 건강보험공단이 보장해야 할 부분을 대신 부담하고 있다. 이는 다음과 같은 과정으로 작동한다:
            </p>
            
            <ol className="list-decimal pl-5 mb-4 space-y-2">
              <li>건강보험공단이 비급여 진료를 통제하면 실손보험이 이익을 얻는다.</li>
              <li>건강보험이 보장해야 할 예비급여 항목을 비급여로 전환하면 건강보험공단이 이익을 얻는다.</li>
              <li>결과적으로 의사의 수입은 감소하고, 국민의 의료비 부담은 증가한다.</li>
            </ol>
          </div>
        </div>
      )}

      {activeTab === 'solutions' && (
        <div>
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <h2 className="text-xl font-bold mb-3 text-gray-800">IV. 결론 및 정책 제언</h2>
            
            <p className="mb-4">
              본 연구는 한국 건강보험 재정의 현황과 구조적 문제점을 분석했다. 주요 발견은 다음과 같다:
            </p>
            
            <ol className="list-decimal pl-5 mb-6 space-y-2">
              <li>건강보험 재정은 표면적으로 흑자를 기록하고 있으나, 재정 운영의 투명성 부족과 불규칙적인 적립 패턴이 심각한 문제로 확인되었다.</li>
              <li>당기순이익과 법정준비금 간의 불일치는 재정 관리의 신뢰성에 의문을 제기한다.</li>
              <li>건강보험의 독과점 구조는 비효율성을 초래하며, 필수의료 서비스의 저수가 문제를 악화시킨다.</li>
              <li>보장률 산출 방식의 조작 가능성이 높으며, 이는 정책 결정의 왜곡을 가져올 수 있다.</li>
              <li>문재인 케어와 실손보험의 구조적 모순은 국민 의료비 부담 증가와 의료 시스템의 지속가능성 위기를 초래하고 있다.</li>
            </ol>

            <h3 className="text-lg font-semibold mb-3 text-gray-700">정책 제언</h3>
            
            <p className="mb-4">
              이러한 문제점을 해결하기 위해 다음과 같은 정책 제언을 제시한다:
            </p>
            
            <div className="mb-6">
              <div className="flex flex-wrap -mx-2">
                <div className="w-full md:w-1/2 px-2 mb-4">
                  <div className="bg-blue-50 p-4 rounded-lg h-full">
                    <h4 className="font-bold text-blue-800 mb-2">1. 재정 운영의 투명성 강화</h4>
                    <p>건강보험 재정 운영에 대한 투명한 정보 공개와 독립적인 감사 체계 구축이 필요하다. 당기순이익의 법정준비금 적립에 대한 명확한 규정과 준수 여부 점검 시스템을 마련해야 한다.</p>
                  </div>
                </div>
                <div className="w-full md:w-1/2 px-2 mb-4">
                  <div className="bg-green-50 p-4 rounded-lg h-full">
                    <h4 className="font-bold text-green-800 mb-2">2. 보장률 산출 방식 개선</h4>
                    <p>비보험 진료를 제외한 급여률 중심의 지표 개발과 전수조사 또는 표준오차를 포함한 통계 발표가 요구된다. 국제 기준에 부합하는 보장성 평가 방법론을 도입해야 한다.</p>
                  </div>
                </div>
                <div className="w-full md:w-1/2 px-2 mb-4">
                  <div className="bg-purple-50 p-4 rounded-lg h-full">
                    <h4 className="font-bold text-purple-800 mb-2">3. 필수의료 수가 현실화</h4>
                    <p>필수의료 서비스에 대한 적정 수가 보장을 통해 의료 시스템의 지속가능성을 확보해야 한다. 의료 인력 수급 계획을 수립하고 필수의료 분야에 대한 지원을 강화해야 한다.</p>
                  </div>
                </div>
                <div className="w-full md:w-1/2 px-2 mb-4">
                  <div className="bg-yellow-50 p-4 rounded-lg h-full">
                    <h4 className="font-bold text-yellow-800 mb-2">4. 건강보험 거버넌스 개혁</h4>
                    <p>독과점 구조의 개선과 의사, 환자 등 이해관계자의 참여를 확대한 거버넌스 체계 구축이 필요하다. 건강보험 정책 결정 과정의 투명성과 책임성을 강화해야 한다.</p>
                  </div>
                </div>
                <div className="w-full px-2 mb-4">
                  <div className="bg-red-50 p-4 rounded-lg">
                    <h4 className="font-bold text-red-800 mb-2">5. 실손보험과 건강보험의 역할 재정립</h4>
                    <p>공적 보장과 민간 보험의 역할을 명확히 구분하고, 비급여 진료에 대한 적절한 관리 체계를 마련해야 한다. 실손보험이 건강보험의 보장성 부족을 대체하는 구조를 개선하여, 국민의 중복 부담을 줄여야 한다.</p>
                  </div>
                </div>
              </div>
            </div>

            <p>
              본 연구의 한계는 공식적으로 공개된 데이터의 제한성과 실제 재정 운영의 세부 내역에 대한 접근 제약에 있다. 향후 연구에서는 좀 더 세부적인 재정 데이터에 기반한 분석과 국제 비교 연구를 통해 한국 건강보험 제도의 개선 방향을 더욱 구체화할 필요가 있다.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <h3 className="font-bold mb-3 text-gray-800">참고문헌</h3>
            <ol className="list-decimal pl-5 space-y-2">
              <li>국민건강보험공단 (2025). 2024년 건강보험 재정현황 보고서.</li>
              <li>보건복지부 (2024). 2023년 건강보험환자 진료비 실태조사.</li>
              <li>미래한국의료정책포럼 (2024). 건강보험공단의 독과점.</li>
              <li>OECD (2024). 건강통계 2024.</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  );
};

export default HealthInsuranceReport;