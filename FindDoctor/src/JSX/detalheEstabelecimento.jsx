import React from 'react'

export default function DetalheEstabelecimento({ estabelecimento, onClose }) {
    const thStyle = {
        textAlign: 'left',
        borderBottom: '1px solid #ccc',
        padding: '4px 8px',
        backgroundColor: '#f2f2f2',
    };

    const tdStyle = {
        padding: '4px 8px',
        borderBottom: '1px solid #eee',
    };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0, left: 0, right: 0, bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
      }}
      onClick={onClose} // fecha se clicar fora do modal
    >
      <div
        style={{
          backgroundColor: 'white',
          padding: '20px',
          borderRadius: '8px',
          width: '750px',
          maxHeight: '80vh',
          overflowY: 'auto',
          boxShadow: '0 2px 10px rgba(0,0,0,0.3)',
          position: 'relative',
        }}
        onClick={e => e.stopPropagation()} // impede fechar ao clicar dentro
      >
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '10px',
            right: '10px',
            border: 'none',
            background: 'transparent',
            fontSize: '18px',
            cursor: 'pointer',
          }}
          aria-label="Fechar"
        >
          ×
        </button>

        <h2>{estabelecimento.nome}</h2>
        <p><b>Código CNES:</b> {estabelecimento.codigoCNES}</p>
        <p><b>CNPJ:</b> {estabelecimento.cnpj}</p>
        <p><b>Endereço:</b> {estabelecimento.endereco}, {estabelecimento.numero}</p>
        <p><b>Bairro:</b> {estabelecimento.bairro}</p>
        <p><b>Cidade:</b> {estabelecimento.cidade}</p>
        <p><b>Estado:</b> {estabelecimento.uf}</p>
        <p><b>Telefone:</b> {estabelecimento.telefone}</p>
        <p><b>Profissionais:</b></p>
        {estabelecimento.profissionais.length > 0 ? (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '8px' }}>
            <thead>
            <tr>
                <th style={thStyle}>Nome</th>
                <th style={thStyle}>CNS</th>
                <th style={thStyle}>Especialidade</th>
            </tr>
            </thead>
            <tbody>
            {estabelecimento.profissionais.map((prof, index) => (
                <tr key={index}>
                <td style={tdStyle}>{prof.nome}</td>
                <td style={tdStyle}>{prof.cns}</td>
                <td style={tdStyle}>{prof.especialidadeNome}</td>
                </tr>
            ))}
            </tbody>
        </table>
        ) : (
        <p style={{ marginTop: '8px' }}>Nenhum profissional encontrado</p>
        )}

      </div>
    </div>
  )
}
