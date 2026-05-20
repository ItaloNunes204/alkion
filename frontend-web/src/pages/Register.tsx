import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import api from "../services/api";

interface Plan {
    id: number;
    name: string;
    description: string;
    monthly_price: number;
    annual_price: number;
    max_stores: number;
    max_users: number;
}

export default function Register() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const planId = searchParams.get("plan");

    const [plan, setPlan] = useState<Plan | null>(null);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState("");
    const [step, setStep] = useState(1);

    const [form, setForm] = useState({
        legal_name: "",
        trade_name: "",
        tax_id: "",
        site: "",
        email: "",
        phone: "",
        responsible: "",
        password: "",
        zip_code: "",
        street: "",
        street_number: "",
        complement: "",
        neighborhood: "",
        city: "",
        state: "",
    });

    useEffect(() => {
        if (planId) {
            api.get(`/api/v1/plans/${planId}`)
                .then((res) => setPlan(res.data))
                .catch(() => setError("Error loading plan."));
        }
    }, [planId]);

    function handleChange(
        e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
    ) {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setLoading(true);
        setError("");

        api.post("/api/v1/companies/register", {
            ...form,
            plan_id: planId ? parseInt(planId) : null,
            billing_cycle: "monthly",
        })
            .then((res) => {
                localStorage.setItem("access_token", res.data.access_token);
                localStorage.setItem("refresh_token", res.data.refresh_token);
                localStorage.setItem(
                    "company",
                    JSON.stringify(res.data.company),
                );
                setSuccess(true);
            })
            .catch((err) =>
                setError(
                    err.response?.data?.erro ||
                        "Error registering. Please try again.",
                ),
            )
            .finally(() => setLoading(false));
    }

    if (success)
        return (
            <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
                <div className="text-center">
                    <div className="text-6xl mb-4">🎉</div>
                    <h2 className="text-3xl font-bold text-green-400 mb-4">
                        Registration complete!
                    </h2>
                    <p className="text-gray-400">
                        You will receive an email with access instructions soon.
                    </p>
                </div>
            </div>
        );

    return (
        <div className="min-h-screen bg-gray-900 text-white px-8 py-16">
            <div className="max-w-5xl mx-auto">
                <button
                    onClick={() => navigate("/plans")}
                    className="text-gray-400 hover:text-white mb-8 flex items-center gap-2 transition"
                >
                    ← Back to plans
                </button>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                    {/* Plano escolhido */}
                    <div>
                        <h2 className="text-xl font-bold mb-4">
                            Selected plan
                        </h2>
                        {plan ? (
                            <div className="bg-gray-800 rounded-xl p-5 border border-blue-500">
                                <h3 className="text-xl font-bold text-blue-400 mb-1">
                                    {plan.name}
                                </h3>
                                <p className="text-gray-400 text-sm mb-3">
                                    {plan.description}
                                </p>
                                <p className="text-3xl font-bold mb-3">
                                    R$ {plan.monthly_price.toFixed(2)}
                                    <span className="text-sm text-gray-400">
                                        /mo
                                    </span>
                                </p>
                                <ul className="text-sm text-gray-300 space-y-1 mb-4">
                                    <li>
                                        ✓ Up to{" "}
                                        {plan.max_stores === 999
                                            ? "unlimited"
                                            : plan.max_stores}{" "}
                                        {plan.max_stores === 1
                                            ? "store"
                                            : "stores"}
                                    </li>
                                    <li>
                                        ✓ Up to{" "}
                                        {plan.max_users === 999
                                            ? "unlimited"
                                            : plan.max_users}{" "}
                                        users per store
                                    </li>
                                    <li>✓ Support included</li>
                                </ul>
                                <button
                                    onClick={() => navigate("/plans")}
                                    className="text-blue-400 hover:text-blue-300 text-sm underline transition"
                                >
                                    Change plan
                                </button>
                            </div>
                        ) : (
                            <div className="bg-gray-800 rounded-xl p-5 border border-gray-700 text-gray-400 text-sm">
                                No plan selected.
                                <button
                                    onClick={() => navigate("/plans")}
                                    className="block text-blue-400 underline mt-2"
                                >
                                    Choose a plan
                                </button>
                            </div>
                        )}

                        {/* Steps */}
                        <div className="mt-8">
                            <p className="text-sm text-gray-400 mb-3">
                                Progress
                            </p>
                            <div className="space-y-2">
                                {["Company data", "Address", "Access"].map(
                                    (label, i) => (
                                        <div
                                            key={i}
                                            className={`flex items-center gap-3 text-sm ${step === i + 1 ? "text-white" : step > i + 1 ? "text-green-400" : "text-gray-500"}`}
                                        >
                                            <div
                                                className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${step === i + 1 ? "bg-blue-600" : step > i + 1 ? "bg-green-600" : "bg-gray-700"}`}
                                            >
                                                {step > i + 1 ? "✓" : i + 1}
                                            </div>
                                            {label}
                                        </div>
                                    ),
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Formulário */}
                    <div className="md:col-span-2">
                        <form onSubmit={handleSubmit}>
                            {/* Step 1 — Company data */}
                            {step === 1 && (
                                <div>
                                    <h2 className="text-2xl font-bold mb-6">
                                        Company data
                                    </h2>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div className="md:col-span-2">
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Legal Name *
                                            </label>
                                            <input
                                                type="text"
                                                name="legal_name"
                                                value={form.legal_name}
                                                onChange={handleChange}
                                                required
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Trade Name
                                            </label>
                                            <input
                                                type="text"
                                                name="trade_name"
                                                value={form.trade_name}
                                                onChange={handleChange}
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Tax ID (CNPJ) *
                                            </label>
                                            <input
                                                type="text"
                                                name="tax_id"
                                                value={form.tax_id}
                                                onChange={handleChange}
                                                required
                                                placeholder="00.000.000/0000-00"
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Phone *
                                            </label>
                                            <input
                                                type="text"
                                                name="phone"
                                                value={form.phone}
                                                onChange={handleChange}
                                                required
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Website
                                            </label>
                                            <input
                                                type="text"
                                                name="site"
                                                value={form.site}
                                                onChange={handleChange}
                                                placeholder="https://"
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div className="md:col-span-2">
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Responsible Person *
                                            </label>
                                            <input
                                                type="text"
                                                name="responsible"
                                                value={form.responsible}
                                                onChange={handleChange}
                                                required
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>
                                    </div>

                                    <button
                                        type="button"
                                        onClick={() => setStep(2)}
                                        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg font-semibold transition"
                                    >
                                        Next →
                                    </button>
                                </div>
                            )}

                            {/* Step 2 — Address */}
                            {step === 2 && (
                                <div>
                                    <h2 className="text-2xl font-bold mb-6">
                                        Address
                                    </h2>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                ZIP Code
                                            </label>
                                            <input
                                                type="text"
                                                name="zip_code"
                                                value={form.zip_code}
                                                onChange={handleChange}
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                State
                                            </label>
                                            <input
                                                type="text"
                                                name="state"
                                                value={form.state}
                                                onChange={handleChange}
                                                maxLength={2}
                                                placeholder="SP"
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div className="md:col-span-2">
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Street
                                            </label>
                                            <input
                                                type="text"
                                                name="street"
                                                value={form.street}
                                                onChange={handleChange}
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Number
                                            </label>
                                            <input
                                                type="text"
                                                name="street_number"
                                                value={form.street_number}
                                                onChange={handleChange}
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Complement
                                            </label>
                                            <input
                                                type="text"
                                                name="complement"
                                                value={form.complement}
                                                onChange={handleChange}
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Neighborhood
                                            </label>
                                            <input
                                                type="text"
                                                name="neighborhood"
                                                value={form.neighborhood}
                                                onChange={handleChange}
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                City
                                            </label>
                                            <input
                                                type="text"
                                                name="city"
                                                value={form.city}
                                                onChange={handleChange}
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>
                                    </div>

                                    <div className="flex gap-4 mt-6">
                                        <button
                                            type="button"
                                            onClick={() => setStep(1)}
                                            className="w-full border border-gray-600 hover:border-gray-400 py-3 rounded-lg font-semibold transition"
                                        >
                                            ← Back
                                        </button>
                                        <button
                                            type="button"
                                            onClick={() => setStep(3)}
                                            className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg font-semibold transition"
                                        >
                                            Next →
                                        </button>
                                    </div>
                                </div>
                            )}

                            {/* Step 3 — Access */}
                            {step === 3 && (
                                <div>
                                    <h2 className="text-2xl font-bold mb-6">
                                        Access credentials
                                    </h2>
                                    <div className="space-y-4">
                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Email *
                                            </label>
                                            <input
                                                type="email"
                                                name="email"
                                                value={form.email}
                                                onChange={handleChange}
                                                required
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm text-gray-400 mb-1">
                                                Password *
                                            </label>
                                            <input
                                                type="password"
                                                name="password"
                                                value={form.password}
                                                onChange={handleChange}
                                                required
                                                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                            />
                                        </div>
                                    </div>

                                    {error && (
                                        <p className="text-red-400 text-sm mt-4">
                                            {error}
                                        </p>
                                    )}

                                    <div className="flex gap-4 mt-6">
                                        <button
                                            type="button"
                                            onClick={() => setStep(2)}
                                            className="w-full border border-gray-600 hover:border-gray-400 py-3 rounded-lg font-semibold transition"
                                        >
                                            ← Back
                                        </button>
                                        <button
                                            type="submit"
                                            disabled={loading}
                                            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-900 py-3 rounded-lg font-semibold transition"
                                        >
                                            {loading
                                                ? "Sending..."
                                                : "Create account"}
                                        </button>
                                    </div>
                                </div>
                            )}
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}
