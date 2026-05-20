import { useEffect, useState } from "react";
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

export default function Plans() {
    const [plans, setPlans] = useState<Plan[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api.get("/api/v1/plans/")
            .then((response) => {
                setPlans(response.data);
            })
            .catch(() => {
                setError(
                    "Erro ao carregar planos. Verifique se o backend está rodando.",
                );
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
                <p className="text-gray-400">Carregando planos...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
                <p className="text-red-400">{error}</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <h1 className="text-4xl font-bold text-center mb-2">Planos</h1>
            <p className="text-gray-400 text-center mb-12">
                Escolha o plano ideal para sua empresa
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
                {plans.map((plan) => (
                    <div
                        key={plan.id}
                        className="bg-gray-800 rounded-xl p-6 border border-gray-700"
                    >
                        <h2 className="text-2xl font-bold mb-2">{plan.name}</h2>
                        <p className="text-gray-400 mb-4">{plan.description}</p>
                        <p className="text-3xl font-bold text-blue-400 mb-1">
                            R$ {plan.monthly_price.toFixed(2)}
                            <span className="text-sm text-gray-400">/mês</span>
                        </p>
                        <p className="text-sm text-gray-500 mb-4">
                            ou R$ {plan.annual_price.toFixed(2)}/ano
                        </p>
                        <ul className="text-sm text-gray-300 space-y-1 mb-6">
                            <li>
                                ✓ Até {plan.max_stores}{" "}
                                {plan.max_stores === 1 ? "loja" : "lojas"}
                            </li>
                            <li>✓ Até {plan.max_users} usuários por loja</li>
                        </ul>
                        <a
                            href="/register"
                            className="block text-center bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg font-semibold transition"
                        >
                            Assinar
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
}
