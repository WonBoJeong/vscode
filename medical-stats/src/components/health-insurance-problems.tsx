import React, { useState } from 'react';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ComposedChart, ReferenceLine, Cell, Area, AreaChart,
  Scatter, ScatterChart, ZAxis
} from 'recharts';

const HealthInsuranceAnalysis = () => {
  const [activeTab, setActiveTab] = useState('accumulation');

  // 건강보험 재정 데이터
  const financialData = [
    { year: '2009', currentSurplus: 311240912, cumulativeSurplus: 311240912, accumulatedReserve: null, difference: null, percentDifference: null },
    { year: '2010', currentSurplus: -977459054, cumulativeSurplus: -666218142, accumulatedReserve: null, difference: null, percentDifference: null },
    { year: '2011', currentSurplus: 1502321489, cumulativeSurplus: 836103347, accumulatedReserve: null, difference: null, percentDifference: null },
    { year: '2012', currentSurplus: 3321608413, cumulativeSurplus: 4157711760, accumulatedReserve: null, difference: null, percentDifference: null },
    { year: '2013', currentSurplus: 5940515756, cumulativeSurplus: 10098227516, accumulatedReserve: null, difference: null, percentDifference: null },
    { year: '2014', currentSurplus: 5762988745, cumulativeSurplus: 15861216261, accumulatedReserve: 12807257170, difference: -3053959091, percentDifference: -19.25 },
    { year: '2015', currentSurplus: 5129941677, cumulativeSurplus: 20991157938, accumulatedReserve: 16980057170, difference: -4011100768, percentDifference: -19.11 },
    { year: '2016', currentSurplus: 2719046232, cumulativeSurplus: 23710204170, accumulatedReserve: 20065657170, difference: -3644547000, percentDifference: -15.37 },
    { year: '2017', currentSurplus: 795511945, cumulativeSurplus: 24505716115, accumulatedReserve: 20773357170, difference: -3732358945, percentDifference: -15.23 },
    { year: '2018', currentSurplus: -3262545727, cumulativeSurplus: 21243170388, accumulatedReserve: 20595513967, difference: -647656421, percentDifference: -3.05 },
    { year: '2019', currentSurplus: -2923973614, cumulativeSurplus: 18319196774, accumulatedReserve: 17771260551, difference: -547936223, percentDifference: -2.99 },
    { year: '2020', currentSurplus: 1496208398, cumulativeSurplus: 19815405172, accumulatedReserve: 17418125038, difference: -2397280134, percentDifference: -12.10 },
    { year: '2021', currentSurplus: 2757064158, cumulativeSurplus: 22572469330, accumulatedReserve: 20241042884, difference: -2331426446, percentDifference: -10.33 },
    { year: '2022', currentSurplus: 4832110368, cumulativeSurplus: 27404579698, accumulatedReserve: 23870062333, difference: -3534517365, percentDifference: -12.90 },
    { year: '2023', currentSurplus: 1686386996, cumulativeSurplus: 29090966694, accumulatedReserve: 27997708334, difference: -1093258360, percentDifference: -3.76 }
  ];

  // 법정준비금 적립률 데이터 계산 (당기순이익 대비 법정준비금 증가)
  const allocationRateData = [];
  let previousReserve = null;

  financialData.forEach(item => {
    if (item.accumulatedReserve !== null && previousReserve !== null) {
      const reserveIncrease = item.accumulatedReserve - previousReserve;
      const allocationRate = item.currentSurplus !== 0 ? +(reserveIncrease / item.currentSurplus * 100).toFixed(2) : null;
      
      allocationRateData.push({
        year: item.year,
        당기순이익: +(item.currentSurplus / 1000000000).toFixed(2), // 조원 단위
        준비금증가액: +(reserveIncrease / 1000000000).toFixed(2), // 조원 단위
        적립률: allocationRate,
        expectedIncrease: item.currentSurplus > 0 ? +(item.currentSurplus / 1000000000).toFixed(2) : 0, // 예상 증가액 (당기순이익이 양수일 때)
        gap: item.currentSurplus > 0 ? 
          +((reserveIncrease - item.currentSurplus) / 1000000000).toFixed(2) : 
          +(reserveIncrease / 1000000000).toFixed(2) // 예상과의 차이
      });
    }
    
    previousReserve = item.accumulatedReserve;
  });

  // 연도별 적립 부족액 누적 데이터
  const cumulativeShortfallData = [];
  let cumulativeShortfall = 0;

  allocationRateData.forEach(item => {
    if (item.당기순이익 > 0 && item.준비금증가액 < item.당기순이익) {
      // 당기순이익이 양수이고 준비금 증가액이 당기순이익보다 적을 경우
      const shortfall = item.당기순이익 - item.준비금증가액;
      cumulativeShortfall += shortfall;
    } else if (item.당기순이익 < 0 && item.준비금증가액 > item.당기순이익) {
      // 당기순이익이 음수이고 준비금 감소액이 당기순이익보다 적을 경우
      const shortfall = Math.abs(item.당기순이익) - Math.abs(item.준비금증가액);
      if (shortfall > 0) cumulativeShortfall += shortfall;
    }

    cumulativeShortfallData.push({
      year: item.year,
      shortfall: item.gap < 0 ? Math.abs(item.gap) : 0,
      cumulativeShortfall: +cumulativeShortfall.toFixed(2)
    });
  });

  // 수익/비용/당기순이익 추이 데이터
  const incomeExpenseData = financialData.map(item => {
    const nextItem = financialData.find(d => d.year === String(Number(item.year) + 1));
    const reserveIncrease = nextItem && item.accumulatedReserve && nextItem.accumulatedReserve ? 
      nextItem.accumulatedReserve - item.accumulatedReserve : null;
    
    return {
      year: item.year,
      당기순이익: +(item.currentSurplus / 1000000000).toFixed(2),
      누적당기순이익: +(item.cumulativeSurplus / 1000000000).toFixed(2),
      누적법정준비금: item.accumulatedReserve ? +(item.accumulatedReserve / 1000000000).toFixed(2) : null,
      법정준비금증가액: reserveIncrease ? +(reserveIncrease / 1000000000).toFixed(2) : null
    };
  });

  // 차트용 데이터 가공 (단위: 조원)
  const chartData = financialData.map(item => ({
    year: item.year,
    당기순이익: item.currentSurplus ? +(item.currentSurplus / 1000000000).toFixed(2) : null,
    누적당기순이익: item.cumulativeSurplus ? +(item.cumulativeSurplus / 1000000000).toFixed(2) : null,
    누적법정준비금: item.accumulatedReserve ? +(item.accumulatedReserve / 1000000000).toFixed(2) : null,
    차이: item.difference ? +(item.difference / 1000000000).toFixed(2) : null,
    '차이(%)': item.percentDifference
  }));

  // 적립률과 당기순이익 관계 데이터
  const allocationRelationData = allocationRateData.map(item => ({
    year: item.year,
    x: item.당기순이익, // x축: 당기순이익
    y: item.적립률, // y축: 적립률
    z: Math.abs(item.준비금증가액), // 버블 크기: 준비금 증가액의 절대값
    name: item.year,
    color: item.gap >= 0 ? '#2ecc71' : '#e74c3c'
  }));

  // 포맷팅 함수
  const formatAmount = (amount) => {
    if (amount === null || amount === undefined) return '-';
    return new Intl.NumberFormat('ko-KR').format(amount);
  };
  
  const formatPercent = (percent) => {
    if (percent === null || percent === undefined) return '-';
    return percent.toFixed(2) + '%';
  };

  const formatTrillion = (amount) => {
    if (amount === null || amount === undefined) return '-';
    return amount.toFixed(2) + '조원';
  };

  // 툴팁 커스텀 컴포넌트
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded shadow-md">
          <p className="font-bold mb-1">{`${label}년`}</p>
          {payload.map((entry, index) => (
            <p key={`item-${index}`} className="text-sm" style={{ color: entry.color }}>
              {`${entry.name}: ${entry.value !== null ? 
                (entry.name.includes('%') ? 
                  entry.value.toFixed(2) + '%' : 
                  entry.value.toFixed(2) + '조원') 
                : '-'}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const ScatterTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded shadow-md">
          <p className="font-bold mb-1">{`${data.name}년`}</p>
          <p className="text-sm">{`당기순이익: ${data.x.toFixed(2)}조원`}</p>
          <p className="text-sm">{`적립률: ${data.y ? data.y.toFixed(2) : 'N/A'}%`}</p>
          <p className="text-sm">{`준비금 증가액: ${data.z.toFixed(2)}조원`}</p>
        </div>
      );
    }
    return null;
  };

  const renderTabContent = () => {
    switch(activeTab) {
      case 'accumulation':
        return (
          <>
            <div className="bg-white p-6 rounded-lg shadow mb-6">
              <h3 className="text-lg font-semibold mb-4">누적 당기순이익과 누적 법정준비금 비교 (조원)</h3>
              <p className="mb-4 text-gray-700">
                이 차트는 연도별 누적 당기순이익과 누적 법정준비금의 추이를 보여줍니다. 
                두 값 사이의 차이가 건강보험 잉여금의 불규칙적인 적립 문제를 나타냅니다.
              </p>
              <ResponsiveContainer width="100%" height={400}>
                <ComposedChart data={chartData.filter(d => d.year >= '2014')} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Area type="monotone" dataKey="누적당기순이익" fill="#8884d8" stroke="#8884d8" fillOpacity={0.3} />
                  <Line type="monotone" dataKey="누적법정준비금" stroke="#2ecc71" dot={{ r: 5 }} strokeWidth={2} />
                  <Bar dataKey="당기순이익" fill="#3498db" opacity={0.7} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>

            <div className="overflow-x-auto mb-6">
              <table className="min-w-full bg-white rounded-lg overflow-hidden shadow">
                <thead className="bg-blue-500 text-white">
                  <tr>
                    <th className="py-3 px-4 text-center">연도</th>
                    <th className="py-3 px-4 text-right">당기순이익<br/>(조원)</th>
                    <th className="py-3 px-4 text-right">누적 당기순이익<br/>(조원)</th>
                    <th className="py-3 px-4 text-right">누적 법정준비금<br/>(조원)</th>
                    <th className="py-3 px-4 text-right">차이<br/>(조원)</th>
                    <th className="py-3 px-4 text-right">차이<br/>(%)</th>
                  </tr>
                </thead>
                <tbody>
                  {chartData.filter(d => d.year >= '2014').map((row, index) => (
                    <tr key={index} className={index === chartData.filter(d => d.year >= '2014').length - 1 ? 'bg-yellow-50 font-bold' : (index % 2 === 0 ? 'bg-gray-50' : '')}>
                      <td className="py-2 px-4 text-center">{row.year}</td>
                      <td className={`py-2 px-4 text-right ${row.당기순이익 >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatTrillion(row.당기순이익)}
                      </td>
                      <td className="py-2 px-4 text-right">{formatTrillion(row.누적당기순이익)}</td>
                      <td className="py-2 px-4 text-right">{formatTrillion(row.누적법정준비금)}</td>
                      <td className={`py-2 px-4 text-right ${row.차이 >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatTrillion(row.차이)}
                      </td>
                      <td className={`py-2 px-4 text-right ${row['차이(%)'] >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatPercent(row['차이(%)'])}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        );
      
      case 'allocation':
        return (
          <>
            <div className="bg-white p-6 rounded-lg shadow mb-6">
              <h3 className="text-lg font-semibold mb-4">당기순이익 대비 법정준비금 적립률 분석</h3>
              <p className="mb-4 text-gray-700">
                이 차트는 연도별 당기순이익 대비 법정준비금 증가액의 비율(적립률)을 보여줍니다. 
                100% 기준선은 당기순이익만큼 법정준비금이 증가했음을 의미합니다.
                적립률이 일정하지 않고 크게 변동하는 것은 건강보험 재정 운영의 불규칙성을 나타냅니다.
              </p>
              <ResponsiveContainer width="100%" height={400}>
                <ComposedChart data={allocationRateData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis domain={[-50, 250]} />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Bar dataKey="당기순이익" name="당기순이익" fill="#3498db" />
                  <Bar dataKey="준비금증가액" name="법정준비금 증가액" fill="#2ecc71">
                    {allocationRateData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.gap >= 0 ? '#2ecc71' : '#e74c3c'} />
                    ))}
                  </Bar>
                  <Line type="monotone" dataKey="적립률" name="적립률(%)" stroke="#ff7300" dot={{ r: 5 }} strokeWidth={2} />
                  <ReferenceLine y={100} stroke="#000" strokeDasharray="3 3" label="적정 적립률(100%)" />
                  <ReferenceLine y={0} stroke="#000" />
                </ComposedChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white p-6 rounded-lg shadow mb-6">
              <h3 className="text-lg font-semibold mb-4">당기순이익과 적립률의 관계 분석</h3>
              <p className="mb-4 text-gray-700">
                이 산점도는 당기순이익(X축)과 적립률(Y축)의 관계를 보여줍니다. 
                버블 크기는 법정준비금 증가액의 절대값을 나타내며, 색상은 준비금 증가액이 당기순이익보다 많으면 초록색, 적으면 빨간색입니다.
                규칙적인 적립이 이루어진다면 점들이 일정한 패턴을 보여야 하지만, 실제로는 매우 불규칙한 분포를 보입니다.
              </p>
              <ResponsiveContainer width="100%" height={400}>
                <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" dataKey="x" name="당기순이익" unit="조원" />
                  <YAxis type="number" dataKey="y" name="적립률" unit="%" domain={[-50, 250]} />
                  <ZAxis type="number" dataKey="z" range={[50, 1000]} />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<ScatterTooltip />} />
                  <Legend />
                  <Scatter name="당기순이익-적립률 관계" data={allocationRelationData} fill="#8884d8">
                    {allocationRelationData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Scatter>
                  <ReferenceLine y={100} stroke="#000" strokeDasharray="3 3" />
                  <ReferenceLine x={0} stroke="#000" />
                </ScatterChart>
              </ResponsiveContainer>
            </div>

            <div className="overflow-x-auto mb-6">
              <table className="min-w-full bg-white rounded-lg overflow-hidden shadow">
                <thead className="bg-blue-500 text-white">
                  <tr>
                    <th className="py-3 px-4 text-center">연도</th>
                    <th className="py-3 px-4 text-right">당기순이익<br/>(조원)</th>
                    <th className="py-3 px-4 text-right">법정준비금 증가액<br/>(조원)</th>
                    <th className="py-3 px-4 text-right">적립률<br/>(%)</th>
                    <th className="py-3 px-4 text-right">예상과의 차이<br/>(조원)</th>
                  </tr>
                </thead>
                <tbody>
                  {allocationRateData.map((row, index) => (
                    <tr key={index} className={index === allocationRateData.length - 1 ? 'bg-yellow-50 font-bold' : (index % 2 === 0 ? 'bg-gray-50' : '')}>
                      <td className="py-2 px-4 text-center">{row.year}</td>
                      <td className={`py-2 px-4 text-right ${row.당기순이익 >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatTrillion(row.당기순이익)}
                      </td>
                      <td className={`py-2 px-4 text-right ${row.준비금증가액 >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatTrillion(row.준비금증가액)}
                      </td>
                      <td className={`py-2 px-4 text-right ${row.적립률 >= 100 ? 'text-green-600' : (row.적립률 >= 0 ? 'text-orange-500' : 'text-red-600')}`}>
                        {formatPercent(row.적립률)}
                      </td>
                      <td className={`py-2 px-4 text-right ${row.gap >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {formatTrillion(row.gap)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        );
      
      case 'shortfall':
        return (
          <>
            <div className="bg-white p-6 rounded-lg shadow mb-6">
              <h3 className="text-lg font-semibold mb-4">연도별 적립 부족액 및 누적 부족액 (조원)</h3>
              <p className="mb-4 text-gray-700">
                이 차트는 당기순이익이 양수일 때 적립되어야 할 금액보다 적게 적립된 부족액을 연도별로 보여줍니다.
                막대 그래프는 연도별 부족액, 선 그래프는 누적 부족액을 나타냅니다.
                누적 부족액이 지속적으로 증가하는 것은 건강보험 잉여금의 일부가 법정준비금으로 적립되지 않고 있음을 시사합니다.
              </p>
              <ResponsiveContainer width="100%" height={400}>
                <ComposedChart data={cumulativeShortfallData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Bar dataKey="shortfall" name="연도별 적립 부족액" fill="#e74c3c" />
                  <Line type="monotone" dataKey="cumulativeShortfall" name="누적 적립 부족액" stroke="#8884d8" dot={{ r: 5 }} strokeWidth={2} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>

            <div className="overflow-x-auto mb-6">
              <table className="min-w-full bg-white rounded-lg overflow-hidden shadow">
                <thead className="bg-blue-500 text-white">
                  <tr>
                    <th className="py-3 px-4 text-center">연도</th>
                    <th className="py-3 px-4 text-right">연도별 적립 부족액<br/>(조원)</th>
                    <th className="py-3 px-4 text-right">누적 적립 부족액<br/>(조원)</th>
                  </tr>
                </thead>
                <tbody>
                  {cumulativeShortfallData.map((row, index) => (
                    <tr key={index} className={index === cumulativeShortfallData.length - 1 ? 'bg-yellow-50 font-bold' : (index % 2 === 0 ? 'bg-gray-50' : '')}>
                      <td className="py-2 px-4 text-center">{row.year}</td>
                      <td className="py-2 px-4 text-right text-red-600">
                        {formatTrillion(row.shortfall)}
                      </td>
                      <td className="py-2 px-4 text-right">
                        {formatTrillion(row.cumulativeShortfall)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-6">건강보험 적립금 문제점 분석</h1>
      
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-3">건강보험 재정 운영의 주요 문제점</h2>
        <ol className="list-decimal pl-6 space-y-3">
          <li>
            <span className="font-semibold">불규칙적인 법정준비금 적립 패턴</span>: 
            <p className="mt-1">당기순이익에 대한 법정준비금 적립률이 -23.60%에서 244.76%까지 연도별로 크게 다르며 일관성이 없습니다.</p>
          </li>
          <li>
            <span className="font-semibold">누적 당기순이익과 누적 법정준비금의 불일치</span>: 
            <p className="mt-1">2023년 기준 누적 당기순이익(29.09조원)과 누적 법정준비금(28.00조원) 간에 1.09조원의 차이가 있으며, 이 차이는 연도별로 큰 변동을 보입니다.</p>
          </li>
          <li>
            <span className="font-semibold">특정 연도의 과다한 미적립 문제</span>: 
            <p className="mt-1">2014-2017년에는 누적 당기순이익의 15-19%가 법정준비금으로 적립되지 않았으며, 2020년에는 당기순이익이 있었음에도 법정준비금이 오히려 감소했습니다.</p>
          </li>
          <li>
            <span className="font-semibold">재정 운영의 투명성 문제</span>: 
            <p className="mt-1">적립되지 않은 자금의 사용처에 대한 명확한 정보가 없어 건강보험 재정 운영의 투명성에 의문이 제기됩니다.</p>
          </li>
        </ol>
      </div>
      
      <div className="flex mb-6 border-b">
        <button 
          className={`px-4 py-2 ${activeTab === 'accumulation' ? 'text-blue-600 border-b-2 border-blue-600 font-medium' : 'text-gray-600'}`}
          onClick={() => setActiveTab('accumulation')}
        >
          누적액 비교
        </button>
        <button 
          className={`px-4 py-2 ${activeTab === 'allocation' ? 'text-blue-600 border-b-2 border-blue-600 font-medium' : 'text-gray-600'}`}
          onClick={() => setActiveTab('allocation')}
        >
          적립률 분석
        </button>
        <button 
          className={`px-4 py-2 ${activeTab === 'shortfall' ? 'text-blue-600 border-b-2 border-blue-600 font-medium' : 'text-gray-600'}`}
          onClick={() => setActiveTab('shortfall')}
        >
          적립 부족액 분석
        </button>
      </div>
      
      {renderTabContent()}
      
      <div className="bg-white p-6 rounded-lg shadow mt-6">
        <h3 className="text-lg font-semibold mb-3">종합 평가</h3>
        <div className="space-y-3">
          <p>
            데이터 분석 결과, 건강보험 재정 운영에 있어 <span className="font-bold">일관성 부재</span>, <span className="font-bold">투명성 부족</span>, <span className="font-bold">누적 불일치</span>, <span className="font-bold">규정 미준수 가능성</span> 등의 문제점이 확인됩니다.
          </p>
          <p>
            특히 당기순이익에 대한 법정준비금 적립률이 연도별로 크게 다르며 일정한 규칙이 없다는 점은 건강보험 재정이 규정대로 처리되지 않고 있음을 시사합니다. 
            2020년의 경우 당기순이익이 1.50조원 발생했음에도 법정준비금은 오히려 0.35조원 감소하는 이례적인 상황이 발생했습니다.
          </p>
          <p>
            2023년에는 당기순이익보다 훨씬 많은 금액이 법정준비금으로 적립되면서 누적 차이가 줄어들고 있는 추세이지만, 
            이전 연도의 불규칙적인 적립 패턴에 대한 설명과 투명한 정보 공개는 여전히 필요한 상황입니다.
          </p>
          <p>
            국민의 건강보험료로 조성된 자금이 어떻게 관리되고 사용되는지에 대한 더 명확한 정보 공개와 일관된 규정 적용이 필요합니다.
          </p>
        </div>
      </div>
      
      <p className="text-sm text-gray-600 mt-4">참고: 금액은 조원 단위로 표시되며, 2009-2013년의 누적 법정준비금 데이터는 원본 자료에서 제공되지 않았습니다.</p>
    </div>
  );
};

export default HealthInsuranceAnalysis;