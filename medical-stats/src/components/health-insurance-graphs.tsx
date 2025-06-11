import React from 'react';
import { 
  LineChart, Line, BarChart, Bar, 
  XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer,
  ComposedChart, Area, ReferenceLine
} from 'recharts';

const HealthInsuranceGraphs = () => {
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

  // 누적 데이터
  const cumulativeData = [
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
    { year: '2017', overall: 62.7, target: 70.0 },
    { year: '2018', overall: 63.8, target: 70.0 },
    { year: '2019', overall: 64.2, target: 70.0 },
    { year: '2020', overall: 65.3, target: 70.0 },
    { year: '2021', overall: 64.5, target: 70.0 },
    { year: '2022', overall: 65.7, target: 70.0 },
    { year: '2023', overall: 64.9, target: 70.0 }
  ];

  // 실손보험 데이터
  const privateInsuranceData = [
    { year: '2021', nonCovered: 7.9, covered: 4.6, total: 12.5 },
    { year: '2022', nonCovered: 7.95, covered: 5.4, total: 13.35 },
    { year: '2023', nonCovered: 8.0, covered: 6.1, total: 14.1 }
  ];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 shadow-md rounded">
          <p className="font-semibold text-gray-800">{`${label}년`}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {`${entry.name}: ${entry.value.toFixed(1)} ${entry.name === 'overall' || entry.name === 'target' ? '%' : '조원'}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="flex flex-col gap-8">
      <div className="w-full h-[500px] bg-white p-4 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4 text-center">그림 1: 건강보험 수입, 지출 및 당기수지 추이 (2009-2023)</h3>
        <ResponsiveContainer width="100%" height="90%">
          <ComposedChart data={financialData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Bar dataKey="income" name="수입" fill="#8884d8" />
            <Bar dataKey="expense" name="지출" fill="#82ca9d" />
            <Line type="monotone" dataKey="balance" name="당기수지차" stroke="#ff7300" strokeWidth={2} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="w-full h-[500px] bg-white p-4 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4 text-center">그림 2: 누적 당기순이익과 누적 법정준비금 비교 (2017-2023)</h3>
        <ResponsiveContainer width="100%" height="90%">
          <ComposedChart data={cumulativeData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Area type="monotone" dataKey="surplus" name="누적 당기순이익" fill="#8884d8" stroke="#8884d8" fillOpacity={0.3} />
            <Area type="monotone" dataKey="reserve" name="누적 법정준비금" fill="#82ca9d" stroke="#82ca9d" fillOpacity={0.3} />
            <Line type="monotone" dataKey="difference" name="차이" stroke="#ff7300" strokeWidth={2} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="w-full h-[500px] bg-white p-4 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4 text-center">그림 3: 건강보험 보장률 추이와 목표치 비교 (2017-2023)</h3>
        <ResponsiveContainer width="100%" height="90%">
          <ComposedChart data={coverageData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis domain={[55, 75]} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Bar dataKey="overall" name="실제 보장률" fill="#8884d8" />
            <ReferenceLine y={70} stroke="red" strokeDasharray="3 3" label={{ value: '목표 보장률 70%', position: 'right' }} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="w-full h-[500px] bg-white p-4 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4 text-center">그림 4: 실손보험 지급 현황 (2021-2023)</h3>
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={privateInsuranceData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Bar dataKey="nonCovered" name="비급여 보험금" stackId="a" fill="#8884d8" />
            <Bar dataKey="covered" name="급여 본인부담금" stackId="a" fill="#82ca9d" />
            <Line dataKey="total" name="총 지급액" stroke="#ff7300" strokeWidth={2} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default HealthInsuranceGraphs;