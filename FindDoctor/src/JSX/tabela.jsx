import React, { useState, useEffect } from 'react'
import { FaInfoCircle } from 'react-icons/fa'
import DetalheEstabelecimento from './detalheEstabelecimento'
import '../CSS/tabela.css'

function Tabela() {
  const [estabelecimentos, setEstabelecimentos] = useState([])
  const [estabelecimentoSelecionado, setEstabelecimentoSelecionado] = useState(null)

  useEffect(() => {
    const handler = (event) => {
      setEstabelecimentos(event.detail)
    }
    window.addEventListener('estabelecimentosAtualizados', handler)
    return () => window.removeEventListener('estabelecimentosAtualizados', handler)
  }, [])

  return (
    <div className="tabela_container" style={{ display: 'flex', gap: '24px' }}>
      <div className="tabela_content" style={{ flex: 1 }}>
        <table className="tabela_infos">
          <thead>
            <tr>
              <th className="tabela_titulo">Estabelecimento</th>
              <th className="tabela_titulo">Rua</th>
              <th className="tabela_titulo">Bairro</th>
              <th className="tabela_titulo">Cidade</th>
              <th className="tabela_titulo">Estado</th>
              <th className="tabela_titulo">Ações</th>
            </tr>
          </thead>
          <tbody>
            {estabelecimentos.length > 0 ? (
              estabelecimentos.map((estab, index) => (
                <tr key={index}>
                  <td className="tabela_dado">{estab.nome}</td>
                  <td className="tabela_dado">{estab.endereco}</td>
                  <td className="tabela_dado">{estab.bairro}</td>
                  <td className="tabela_dado">{(estab.cidade).toUpperCase()}</td>
                  <td className="tabela_dado">{estab.uf}</td>
                  <td className="tabela_dado">
                    <button
                      onClick={() => setEstabelecimentoSelecionado(estab)}
                      style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                      title="Ver detalhes"
                    >
                      <FaInfoCircle color="#007bff" size={18} />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center' }}>Nenhum estabelecimento encontrado.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {estabelecimentoSelecionado && (
        <DetalheEstabelecimento
          estabelecimento={estabelecimentoSelecionado}
          onClose={() => setEstabelecimentoSelecionado(null)}
        />
      )}
    </div>
  )
}

export default Tabela
