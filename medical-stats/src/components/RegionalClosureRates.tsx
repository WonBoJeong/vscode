import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

interface DataItem {
  region: string;
  rate: number;
  category: string;
}

interface SpecialtyItem {
  specialty: string;
  rate: number;
}

const RegionalClosureRates: React.FC = () => {
  // 지역별 폐업률 데이터 (개업 대비 폐업률, %)
  const data: DataItem[] = [
    { region: '전남', rate: 110.6, category: '지방' },
    { region: '울산', rate: 108.7, category: '지방' },
    { region: '충북', rate: 97.6, category: '지방' },
    { region: '경남', rate: 89.2, category: '지방' },
    { region: '전북', rate: 88.5, category: '지방' },
    { region: '광주', rate: 83.6, category: '지방' },
    { region: '서울', rate: 68.3, category: '수도권' },
    { region: '경기', rate: 65.3, category: '수도권' },
    { region: '인천', rate: 60.8, category: '수도권' }
  ].sort((a, b) => b.rate - a.rate); // 폐업률 기준 내림차순 정렬

  // 의원급 개폐업 격차(2020~2024년) 데이터
  const clinicData: DataItem[] = [
    { region: '전남', rate: 90.3, category: '지방' },
    { region: '경북', rate: 81.9, category: '지방' },
    { region: '충북', rate: 77.2, category: '지방' },
    { region: '경남', rate: 75.7, category: '지방' },
    { region: '서울', rate: 52.8, category: '수도권' },
    { region: '인천', rate: 49.6, category: '수도권' },
    { region: '경기', rate: 45.1, category: '수도권' }
  ].sort((a, b) => b.rate - a.rate); // 폐업률 기준 내림차순 정렬

  // 진료과목별 개폐업 현황(2020~2024년) 데이터
  const specialtyData: SpecialtyItem[] = [
    { specialty: '소아청소년과', rate: 104.9 },
    { specialty: '산부인과', rate: 88.3 },
    { specialty: '정형외과', rate: 39.6 },
    { specialty: '내과', rate: 34.9 },
    { specialty: '신경과', rate: 17.5 },
    { specialty: '정신건강의학과', rate: 15.1 }
  ].sort((a, b) => b.rate - a.rate);

  // 색상 설정
  const getBarColor = (category: string): string => {
    return category === '지방' ? '#FF6B6B' : '#4D96FF';
  };

  return (
    <div className="flex flex-col space-y-8">
      <div>
        <h2 className="text-xl font-bold mb-4">지역별 의료기관 폐업률 (2023년)</h2>
        <p className="text-sm mb-4">개업 대비 폐업률(%): 폐업 의료기관 수 ÷ 개업 의료기관 수 × 100</p>
        <div style={{ height: '400px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" angle={-45} textAnchor="end" height={60} />
              <YAxis domain={[0, 120]} label={{ value: '폐업률(%)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value) => [`${value}%`, '폐업률']} />
              <Legend />
              <Bar dataKey="rate" name="폐업률(%)">
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getBarColor(entry.category)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', marginRight: '16px' }}>
            <div style={{ width: '16px', height: '16px', backgroundColor: '#FF6B6B', marginRight: '4px' }}></div>
            <span>지방</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ width: '16px', height: '16px', backgroundColor: '#4D96FF', marginRight: '4px' }}></div>
            <span>수도권</span>
          </div>
        </div>
        <p className="text-sm mt-4">
          * 폐업률이 100%를 초과하는 지역은 개업보다 폐업이 더 많은 지역입니다.
        </p>
      </div>

      <div>
        <h2 className="text-xl font-bold mb-4">의원급 의료기관 폐업률 (2020~2024년)</h2>
        <div style={{ height: '400px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={clinicData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" angle={-45} textAnchor="end" height={60} />
              <YAxis domain={[0, 100]} label={{ value: '폐업률(%)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value) => [`${value}%`, '폐업률']} />
              <Legend />
              <Bar dataKey="rate" name="폐업률(%)">
                {clinicData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getBarColor(entry.category)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div>
        <h2 className="text-xl font-bold mb-4">진료과목별 폐업률 (2020~2024년)</h2>
        <div style={{ height: '400px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={specialtyData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="specialty" angle={-45} textAnchor="end" height={60} />
              <YAxis domain={[0, 120]} label={{ value: '폐업률(%)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value) => [`${value}%`, '폐업률']} />
              <Legend />
              <Bar dataKey="rate" name="폐업률(%)" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <p className="text-sm mt-4">
          * 소아청소년과는 폐업률이 100%를 초과하여 개업보다 폐업이 더 많은 진료과목입니다.
        </p>
      </div>
    </div>
  );
};

export default RegionalClosureRates;
