// src/DataFetcher.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DataFetcher = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/');
                setData(response.data); // This is your JSON response
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    // Assuming the response structure is correct:
    return (
        <div>
            <h1>Data from FastAPI:</h1>
            <p>{data.message}</p>
            <p>Status: {data.status}</p>
            <h2>Item Details:</h2>
            <p>ID: {data.data.id}</p>
            <p>Name: {data.data.name}</p>
        </div>
    );
};

export default DataFetcher;
