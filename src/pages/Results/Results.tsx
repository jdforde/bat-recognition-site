import React, { PureComponent } from 'react';
import styles from '../Results/Results.module.css'
import {
    ComposedChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    RadialBarChart,
    RadialBar,
  } from 'recharts';

const Results = () => {
    const data = [
        {minutesPassed: 0.0, batCount: 0, in: 0, out: 0},
        {minutesPassed: 22.93, batCount: -1, in: 0, out: 1},
        {minutesPassed: 25.13, batCount: 0, in: 1, out: 1},
        {minutesPassed: 25.75, batCount: -1, in: 1, out: 2},
        {minutesPassed: 26.35, batCount: 0, in: 2, out: 2},
        {minutesPassed: 26.70, batCount: -1, in: 2, out: 3},
        {minutesPassed: 30.28, batCount: 0, in: 3, out: 3},
        {minutesPassed: 35.02, batCount: 1, in: 4, out: 3},
        {minutesPassed: 35.55, batCount: 2, in: 5, out: 3},
        {minutesPassed: 37.75, batCount: 3, in: 6, out: 3},
        {minutesPassed: 44.83, batCount: 4, in: 7, out: 3},
        {minutesPassed: 45.97, batCount: 3, in: 7, out: 4},
        {minutesPassed: 47.50, batCount: 2, in: 7, out: 5},
        {minutesPassed: 48.48, batCount: 3, in: 8, out: 5},
        {minutesPassed: 48.50, batCount: 4, in: 9, out: 5},
        {minutesPassed: 49.67, batCount: 3, in: 9, out: 6},
        {minutesPassed: 49.90, batCount: 2, in: 9, out: 7},
        {minutesPassed: 49.92, batCount: 1, in: 9, out: 8},
        {minutesPassed: 51.48, batCount: 2, in: 10, out: 8},
        {minutesPassed: 52.90, batCount: 3, in: 11, out: 8},
        {minutesPassed: 52.92, batCount: 4, in: 12, out: 8},
        {minutesPassed: 54.10, batCount: 3, in: 12, out: 9},
        {minutesPassed: 54.60, batCount: 2, in: 12, out: 10},
        {minutesPassed: 54.62, batCount: 1, in: 12, out: 11},
        {minutesPassed: 56.18, batCount: 2, in: 13, out: 11},
        {minutesPassed: 57.03, batCount: 3, in: 14, out: 11},
        {minutesPassed: 57.03, batCount: 2, in: 14, out: 12},
        {minutesPassed: 59.62, batCount: 3, in: 15, out: 12}
    ];

    const data2 = [
        {name: "in", total: 15},
        {name: "out", total: 12}
    ];

    const renderChart = (
        <ResponsiveContainer width="100%" height="70%">
            <ComposedChart width={400} height={200} margin={{ top: 5, right: 100, bottom: 5, left: 100 }} data={data}>
                <CartesianGrid stroke="#61ccae"/>
                <XAxis dataKey="minutesPassed" scale="auto" />
                <YAxis dataKey="batCount" scale="linear" />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="batCount" stroke="#ffb5ce" />
                <Line type="monotone" dataKey="in" stroke="#ff6b65" />
                <Line type="monotone" dataKey="out" stroke="#36454F" />
            </ComposedChart>
        </ResponsiveContainer>
    );

    const renderBarChart = (
        <ResponsiveContainer width="100%" height="70%">
            <RadialBarChart width={730} height={250} innerRadius="10%" outerRadius="80%" data={data2} startAngle={180} endAngle={0}>
                <RadialBar label={{ fill: '#36454F', position: 'insideStart' }} background dataKey='total' fill="#61ccae"/>
                <Legend iconSize={10} width={120} height={140} layout='vertical' verticalAlign='middle' align="right" />
                <Tooltip />
            </RadialBarChart>
        </ResponsiveContainer>
    );

    return (
        <div className={styles.image}>
            <div className={styles.formRow}>
                <div className={styles.sidePanel}>
                    <h1 className={styles.title}>Select Data Range</h1>
                    <div className={styles.forms}>
                        <div className={styles.formRow}>
                            <h3 className={styles.identifier}>Start Date: </h3>
                            <select className={styles.input}>
                                <option value="date1">10/06/2021</option>
                                <option value="date2">11/04/2021</option>
                                <option value="date3">12/04/2021</option>
                            </select> 
                        </div>
                        <div className={styles.formRow}>
                            <h3 className={styles.identifier}>End Date: </h3>
                            <select className={styles.input}>
                                <option value="date1">10/06/2021</option>
                                <option value="date2">11/04/2021</option>
                                <option value="date3">12/04/2021</option>
                            </select>
                        </div>
                    </div>
                    <button className={styles.submitButton}>Submit</button>
                </div>
                <div className={styles.contentBox}>
                    <h1 className={styles.title}>Emergence Count Results</h1>
                    <h4 className={styles.subtitle}>Graphical representation of emergence count results within the given time window</h4>
                    {renderChart}
                </div>
            </div>
            
        </div>
    )
};

export default Results;