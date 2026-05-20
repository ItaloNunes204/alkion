import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

interface Plan {
    id: number;
    name: string;
    description: string;
    monthly_price: number;
    annual_price: number;
    max_stores: number;
    max_users: number;
    is_highlighted: boolean;
}

export default function Plans() {
    const [plans, setPlans] = useState<Plan[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [ciclo, setCiclo] = useState<"monthly" | "annual">("monthly");
    const navigate = useNavigate();

    useEffect(() => {
        api.get("/api/v1/plans/")
            .then((res) => setPlans(res.data))
            .catch(() =>
                setError(
                    "Erro ao carregar planos. Verifique se o backend esta rodando.",
                ),
            )
            .finally(() => setLoading(false));
    }, []);

    if (loading)
        return (
            <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
                <p className="text-gray-400">Carregando planos...</p>
            </div>
        );

    if (error)
        return (
            <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
                <p className="text-red-400">{error}</p>
            </div>
        );

    return (
        <div className="min-h-screen bg-gray-900 text-white px-8 py-16">
            {/* Cabecalho */}
            <div className="text-center mb-10">
                <h1 className="text-4xl font-bold mb-2">Planos</h1>
                <p className="text-gray-400 mb-8">
                    Escolha o plano ideal para sua empresa
                </p>

                {/* Toggle mensal / anual */}
                <div className="inline-flex bg-gray-800 rounded-lg p-1">
                    <button
                        onClick={() => setCiclo("monthly")}
                        className={`px-6 py-2 rounded-md font-semibold transition ${
                            ciclo === "monthly"
                                ? "bg-blue-600 text-white"
                                : "text-gray-400 hover:text-white"
                        }`}
                    >
                        Mensal
                    </button>
                    <button
                        onClick={() => setCiclo("annual")}
                        className={`px-6 py-2 rounded-md font-semibold transition ${
                            ciclo === "annual"
                                ? "bg-blue-600 text-white"
                                : "text-gray-400 hover:text-white"
                        }`}
                    >
                        Anual{" "}
                        <span className="text-green-400 text-xs ml-1">
                            -17%
                        </span>
                    </button>
                </div>
            </div>

            {/* Cards dos planos */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto mb-12">
                {plans.map((plan) => (
                    <div
                        key={plan.id}
                        className={`bg-gray-800 rounded-xl p-6 border transition ${
                            plan.is_highlighted
                                ? "border-blue-500 ring-2 ring-blue-500"
                                : "border-gray-700"
                        }`}
                    >
                        {plan.is_highlighted && (
                            <div className="text-center mb-3">
                                <span className="bg-blue-600 text-xs font-bold px-3 py-1 rounded-full">
                                    MAIS POPULAR
                                </span>
                            </div>
                        )}

                        <h2 className="text-2xl font-bold mb-1">{plan.name}</h2>
                        <p className="text-gray-400 text-sm mb-4">
                            {plan.description}
                        </p>

                        <p className="text-4xl font-bold text-blue-400 mb-1">
                            R${" "}
                            {ciclo === "monthly"
                                ? plan.monthly_price.toFixed(2)
                                : (plan.annual_price / 12).toFixed(2)}
                            <span className="text-sm text-gray-400">/mes</span>
                        </p>

                        {ciclo === "annual" && (
                            <p className="text-sm text-green-400 mb-4">
                                R$ {plan.annual_price.toFixed(2)}/ano — 2 meses
                                gratis
                            </p>
                        )}

                        <ul className="text-sm text-gray-300 space-y-2 mb-6 mt-4">
                            <li>
                                ✓ Ate{" "}
                                {plan.max_stores === 999
                                    ? "ilimitadas"
                                    : plan.max_stores}{" "}
                                {plan.max_stores === 1 ? "loja" : "lojas"}
                            </li>
                            <li>
                                ✓ Ate{" "}
                                {plan.max_users === 999
                                    ? "ilimitados"
                                    : plan.max_users}{" "}
                                usuarios por loja
                            </li>
                            <li>✓ Suporte por email</li>
                            {plan.name !== "Starter" && (
                                <li>✓ Suporte prioritario</li>
                            )}
                            {plan.name === "Enterprise" && (
                                <li>✓ Gerente de conta dedicado</li>
                            )}
                        </ul>

                        <button
                            onClick={() =>
                                navigate(`/register?plan=${plan.id}`)
                            }
                            className={`w-full py-3 rounded-lg font-semibold transition ${
                                plan.is_highlighted
                                    ? "bg-blue-600 hover:bg-blue-700"
                                    : "border border-gray-600 hover:border-gray-400"
                            }`}
                        >
                            Assinar
                        </button>
                    </div>
                ))}
            </div>

            {/* Botao comparar */}
            <div className="text-center">
                <button
                    onClick={() => alert("Comparativo detalhado em breve!")}
                    className="text-blue-400 hover:text-blue-300 underline text-sm transition"
                >
                    Comparar todos os planos em detalhes
                </button>
            </div>
        </div>
    );
}
