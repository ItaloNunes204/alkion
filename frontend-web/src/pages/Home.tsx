import { useNavigate } from "react-router-dom";

export default function Home() {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-gray-900 text-white">
            {/* Hero */}
            <div className="flex flex-col items-center justify-center text-center px-8 py-24">
                <h1 className="text-6xl font-bold mb-4">Alkion</h1>
                <p className="text-2xl text-gray-400 mb-4">
                    Sistema de gestao para o varejo alimentar
                </p>
                <p className="text-gray-500 max-w-2xl mb-10">
                    Plataforma completa para supermercados, padarias, acougues e
                    distribuidoras. Gerencie suas lojas, vendas, estoque e muito
                    mais em um unico lugar.
                </p>
                <button
                    onClick={() => navigate("/plans")}
                    className="bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-lg font-bold text-lg transition"
                >
                    Ver Planos
                </button>
            </div>

            {/* Funcionalidades */}
            <div className="max-w-6xl mx-auto px-8 pb-24">
                <h2 className="text-3xl font-bold text-center mb-12">
                    Tudo que sua empresa precisa
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div className="text-3xl mb-3">🛒</div>
                        <h3 className="text-xl font-bold mb-2">PDV Completo</h3>
                        <p className="text-gray-400 text-sm">
                            Frente de caixa moderna com suporte a NF-e, NFC-e,
                            TEF, Pix e todas as formas de pagamento.
                        </p>
                    </div>

                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div className="text-3xl mb-3">📦</div>
                        <h3 className="text-xl font-bold mb-2">
                            Gestao de Estoque
                        </h3>
                        <p className="text-gray-400 text-sm">
                            Controle de produtos, validade, inventario rotativo
                            e alertas de ruptura em tempo real.
                        </p>
                    </div>

                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div className="text-3xl mb-3">📊</div>
                        <h3 className="text-xl font-bold mb-2">
                            Business Intelligence
                        </h3>
                        <p className="text-gray-400 text-sm">
                            Dashboards e relatorios completos para tomar
                            decisoes baseadas em dados precisos.
                        </p>
                    </div>

                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div className="text-3xl mb-3">💰</div>
                        <h3 className="text-xl font-bold mb-2">Financeiro</h3>
                        <p className="text-gray-400 text-sm">
                            Controle de contas, fluxo de caixa, conciliacao
                            bancaria e gestao de cartoes.
                        </p>
                    </div>

                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div className="text-3xl mb-3">📄</div>
                        <h3 className="text-xl font-bold mb-2">Fiscal</h3>
                        <p className="text-gray-400 text-sm">
                            Emissao de NF-e, NFC-e, SPED, apuracao de impostos e
                            conformidade com a legislacao brasileira.
                        </p>
                    </div>

                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <div className="text-3xl mb-3">📱</div>
                        <h3 className="text-xl font-bold mb-2">Multicanal</h3>
                        <p className="text-gray-400 text-sm">
                            Acesse pelo navegador, aplicativo mobile ou desktop.
                            Funciona mesmo sem internet.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
