import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle, Info, XCircle } from 'lucide-react';

const Home = () => {
    const chartData = [
        { name: 'Jan', uv: 4000, pv: 2400, amt: 2400 },
        { name: 'Feb', uv: 3000, pv: 1398, amt: 2210 },
        { name: 'Mar', uv: 2000, pv: 9800, amt: 2290 },
        { name: 'Apr', uv: 2780, pv: 3908, amt: 2000 },
        { name: 'May', uv: 1890, pv: 4800, amt: 2181 },
        { name: 'Jun', uv: 2390, pv: 3800, amt: 2500 },
        { name: 'Jul', uv: 3490, pv: 4300, amt: 2100 },
    ];

    return (
        <div className="min-h-screen bg-neutral-100">
            <div className="navbar bg-primary-700 text-primary-50 shadow-lg">
                <div className="flex-1">
                    <a className="btn btn-ghost normal-case text-xl">Component Showcase</a>
                </div>
            </div>

            <div className="p-8">
                <h1 className="text-4xl font-bold mb-8 text-neutral-800">Component Showcase</h1>

                {/* Buttons Section */}
                <section className="mb-12 bg-primary-50 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-primary-800">Buttons with Different Sizes</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div className="space-y-2">
                            <h3 className="text-lg font-medium mb-2">Primary</h3>
                            <button className="btn btn-primary btn-xs w-full">Extra Small</button>
                            <button className="btn btn-primary btn-sm w-full">Small</button>
                            <button className="btn btn-primary w-full">Normal</button>
                            <button className="btn btn-primary btn-lg w-full">Large</button>
                        </div>
                        <div className="space-y-2">
                            <h3 className="text-lg font-medium mb-2">Secondary</h3>
                            <button className="btn btn-secondary btn-xs w-full">Extra Small</button>
                            <button className="btn btn-secondary btn-sm w-full">Small</button>
                            <button className="btn btn-secondary w-full">Normal</button>
                            <button className="btn btn-secondary btn-lg w-full">Large</button>
                        </div>
                        <div className="space-y-2">
                            <h3 className="text-lg font-medium mb-2">Accent</h3>
                            <button className="btn btn-accent btn-xs w-full">Extra Small</button>
                            <button className="btn btn-accent btn-sm w-full">Small</button>
                            <button className="btn btn-accent w-full">Normal</button>
                            <button className="btn btn-accent btn-lg w-full">Large</button>
                        </div>
                        <div className="space-y-2">
                            <h3 className="text-lg font-medium mb-2">Neutral</h3>
                            <button className="btn btn-neutral btn-xs w-full">Extra Small</button>
                            <button className="btn btn-neutral btn-sm w-full">Small</button>
                            <button className="btn btn-neutral w-full">Normal</button>
                            <button className="btn btn-neutral btn-lg w-full">Large</button>
                        </div>
                    </div>
                </section>

                {/* Dropdowns Section */}
                <section className="mb-12 bg-secondary-50 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-secondary-800">Dropdowns</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div className="dropdown">
                            <label tabIndex={0} className="btn btn-primary m-1">Primary Dropdown</label>
                            <ul tabIndex={0} className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                                <li><a>Item 1</a></li>
                                <li><a>Item 2</a></li>
                            </ul>
                        </div>
                        <div className="dropdown">
                            <label tabIndex={0} className="btn btn-secondary m-1">Secondary Dropdown</label>
                            <ul tabIndex={0} className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                                <li><a>Item 1</a></li>
                                <li><a>Item 2</a></li>
                            </ul>
                        </div>
                    </div>
                </section>

                {/* Alerts Section */}
                <section className="mb-12 bg-accent-50 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-accent-800">Alerts</h2>
                    <div className="space-y-4">
                        <div className="alert alert-info bg-primary-100 text-primary-800">
                            <Info className="text-primary-500"/>
                            <span>New software update available.</span>
                        </div>
                        <div className="alert alert-success bg-accent-100 text-accent-800">
                            <CheckCircle className="text-accent-500" />
                            <span>Your payment has been successfully processed.</span>
                        </div>
                        <div className="alert alert-warning bg-secondary-100 text-secondary-800">
                            <AlertCircle className="text-secondary-500" />
                            <span>Warning: Your subscription is about to expire.</span>
                        </div>
                        <div className="alert alert-error bg-neutral-200 text-neutral-800">
                            <XCircle className="text-neutral-500" />
                            <span>Error: Unable to connect to the server.</span>
                        </div>
                    </div>
                </section>

                {/* Chat Bubbles Section */}
                <section className="mb-12 bg-neutral-50 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-neutral-800">Chat Bubbles</h2>
                    <div className="space-y-4">
                        <div className="chat chat-start">
                            <div className="chat-bubble chat-bubble-primary">Primary bubble</div>
                        </div>
                        <div className="chat chat-end">
                            <div className="chat-bubble chat-bubble-secondary">Secondary bubble</div>
                        </div>
                        <div className="chat chat-start">
                            <div className="chat-bubble chat-bubble-accent">Accent bubble</div>
                        </div>
                        <div className="chat chat-end">
                            <div className="chat-bubble chat-bubble-neutral">Neutral bubble</div>
                        </div>
                    </div>
                </section>

                {/* Checkboxes Section */}
                <section className="mb-12 bg-primary-100 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-primary-800">Checkboxes</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        <label className="flex items-center space-x-2">
                            <input type="checkbox" className="checkbox checkbox-primary" />
                            <span className="text-primary-700">Primary</span>
                        </label>
                        <label className="flex items-center space-x-2">
                            <input type="checkbox" className="checkbox checkbox-secondary" />
                            <span className="text-secondary-700">Secondary</span>
                        </label>
                        <label className="flex items-center space-x-2">
                            <input type="checkbox" className="checkbox checkbox-accent" />
                            <span className="text-accent-700">Accent</span>
                        </label>
                        <label className="flex items-center space-x-2">
                            <input type="checkbox" className="checkbox checkbox-neutral" />
                            <span className="text-neutral-700">Neutral</span>
                        </label>
                    </div>
                </section>

                {/* Text Inputs Section */}
                <section className="mb-12 bg-secondary-100 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-secondary-800">Text Inputs</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <input type="text" placeholder="Primary input" className="input input-bordered input-primary w-full" />
                        <input type="text" placeholder="Secondary input" className="input input-bordered input-secondary w-full" />
                        <input type="text" placeholder="Accent input" className="input input-bordered input-accent w-full" />
                        <input type="text" placeholder="Neutral input" className="input input-bordered input-neutral w-full" />
                    </div>
                </section>

                {/* Loading Section */}
                <section className="mb-12 bg-accent-100 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-accent-800">Loading</h2>
                    <div className="flex flex-wrap gap-4">
                        <span className="loading loading-spinner loading-lg text-primary"></span>
                        <span className="loading loading-dots loading-lg text-secondary"></span>
                        <span className="loading loading-ring loading-lg text-accent"></span>
                        <span className="loading loading-ball loading-lg text-neutral"></span>
                    </div>
                </section>

                {/* Slider Section */}
                <section className="mb-12 bg-neutral-200 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-neutral-800">Sliders</h2>
                    <div className="space-y-4">
                        <input type="range" min="0" max="100" className="range range-primary" />
                        <input type="range" min="0" max="100" className="range range-secondary" />
                        <input type="range" min="0" max="100" className="range range-accent" />
                        <input type="range" min="0" max="100" className="range range-neutral" />
                    </div>
                </section>

                {/* Chart Section */}
                <section className="mb-12 bg-primary-200 p-6 rounded-lg">
                    <h2 className="text-2xl font-semibold mb-4 text-primary-800">Chart</h2>
                    <div className="w-full h-96 bg-white p-4 rounded-lg shadow">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart
                                data={chartData}
                                margin={{
                                    top: 5,
                                    right: 30,
                                    left: 20,
                                    bottom: 5,
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="pv" stroke="#0ea5e9" activeDot={{ r: 8 }} />
                                <Line type="monotone" dataKey="uv" stroke="#d946ef" />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </section>
            </div>

            <footer className="footer p-10 bg-neutral-800 text-neutral-200">
                <div>
                    <span className="footer-title">Services</span>
                    <a className="link link-hover">Branding</a>
                    <a className="link link-hover">Design</a>
                    <a className="link link-hover">Marketing</a>
                    <a className="link link-hover">Advertisement</a>
                </div>
                <div>
                    <span className="footer-title">Company</span>
                    <a className="link link-hover">About us</a>
                    <a className="link link-hover">Contact</a>
                    <a className="link link-hover">Jobs</a>
                    <a className="link link-hover">Press kit</a>
                </div>
                <div>
                    <span className="footer-title">Legal</span>
                    <a className="link link-hover">Terms of use</a>
                    <a className="link link-hover">Privacy policy</a>
                    <a className="link link-hover">Cookie policy</a>
                </div>
            </footer>
        </div>
    );
};

export default Home;