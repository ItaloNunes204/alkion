export default function Home() {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-8">
      <h1 className="text-5xl font-bold mb-4">Alkion</h1>
      <p className="text-xl text-gray-400 mb-2">
        Sistema de gestao para o varejo alimentar
      </p>
      <p className="text-gray-500 max-w-xl text-center mb-8">
        Gerencie suas lojas, vendas, estoque, financeiro e muito mais
        em uma unica plataforma integrada.
      </p>
      <div className="flex gap-4">
        <a href="/plans" className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition">
          Ver Planos
        </a>
        <a href="/register" className="border border-gray-600 hover:border-gray-400 px-6 py-3 rounded-lg font-semibold transition">
          Criar Conta
        </a>
      </div>
    </div>
  )
}