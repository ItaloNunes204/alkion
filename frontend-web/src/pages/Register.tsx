import { useState } from "react";
import api from "../services/api";

export default function Register() {
    const [form, setForm] = useState({
        company_name: "",
        cnpj: "",
        email: "",
        phone: "",
        responsible: "",
        password: "",
    });
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState("");

    // Atualiza o campo do formulário conforme o usuário digita
    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    // Envia o formulário para o backend
    function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setLoading(true);
        setError("");

        api.post("/api/v1/companies/register", form)
            .then(() => {
                setSuccess(true);
            })
            .catch((err) => {
                setError(
                    err.response?.data?.erro ||
                        "Erro ao cadastrar. Tente novamente.",
                );
            })
            .finally(() => {
                setLoading(false);
            });
    }

    if (success) {
        return (
            <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-3xl font-bold text-green-400 mb-4">
                        Cadastro realizado!
                    </h2>
                    <p className="text-gray-400">
                        Em breve você receberá um email com as instruções de
                        acesso.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-8">
            <div className="w-full max-w-md">
                <h1 className="text-3xl font-bold mb-2">Criar conta</h1>
                <p className="text-gray-400 mb-8">
                    Preencha os dados da sua empresa para começar
                </p>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm text-gray-400 mb-1">
                            Razão Social
                        </label>
                        <input
                            type="text"
                            name="company_name"
                            value={form.company_name}
                            onChange={handleChange}
                            required
                            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                        />
                    </div>

                    <div>
                        <label className="block text-sm text-gray-400 mb-1">
                            CNPJ
                        </label>
                        <input
                            type="text"
                            name="cnpj"
                            value={form.cnpj}
                            onChange={handleChange}
                            required
                            placeholder="00.000.000/0000-00"
                            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                        />
                    </div>

                    <div>
                        <label className="block text-sm text-gray-400 mb-1">
                            Responsável
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

                    <div>
                        <label className="block text-sm text-gray-400 mb-1">
                            Email
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
                            Telefone
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
                            Senha
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

                    {error && <p className="text-red-400 text-sm">{error}</p>}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-900 px-4 py-3 rounded-lg font-semibold transition"
                    >
                        {loading ? "Enviando..." : "Criar conta"}
                    </button>
                </form>
            </div>
        </div>
    );
}
