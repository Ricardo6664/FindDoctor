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
    <div className="tabela_container" style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', marginLeft: '50px', marginRight: '50px', marginBottom: '10px' }}>
      <div className="tabela_content" style={{ flex: 1, minWidth: '300px', overflowX: 'auto' }}>
        <table className="tabela_infos modern">
          <thead>
            <tr>
              <th>Estabelecimento</th>
              <th>Rua</th>
              <th>Bairro</th>
              <th>Cidade</th>
              <th>Estado</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {estabelecimentos.length > 0 ? (
              estabelecimentos.map((estab, index) => (
                <tr key={index}>
                  <td>{estab.nome}</td>
                  <td>{estab.endereco}</td>
                  <td>{estab.bairro}</td>
                  <td>{estab.cidade.toUpperCase()}</td>
                  <td>{estab.uf}</td>
                  <td>
                    <button
                      onClick={() => setEstabelecimentoSelecionado(estab)}
                      className="btn_info"
                      title="Ver detalhes"
                    >
                      <FaInfoCircle size={18} />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', padding: '20px' }}>
                  Nenhum estabelecimento encontrado.
                </td>
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
