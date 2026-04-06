'use client'

import { useState } from 'react'
import { contractApi } from '@/lib/api'

interface DownloadInfo {
  id: string
  name: string
  download_id: string
}

interface DownloadStepProps {
  documentId: string
  onReset: () => void
  documents?: DownloadInfo[]
}

type DownloadFormat = 'pdf' | 'docx'

export default function DownloadStep({ documentId, onReset, documents }: DownloadStepProps) {
  const [downloadingKey, setDownloadingKey] = useState<string | null>(null)

  const getCondicoesGeraisId = (): string | null => {
    if (documents && documents.length > 0) {
      const condicoesDoc = documents.find(doc => doc.id === 'condicoes_gerais')
      if (condicoesDoc) {
        return condicoesDoc.download_id
      }
    }

    const quadroSuffix = '_quadro_resumo'
    if (documentId.endsWith(quadroSuffix)) {
      const baseId = documentId.slice(0, -quadroSuffix.length)
      return `${baseId}_condicoes_gerais`
    }

    const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i
    const match = documentId.match(uuidPattern)
    if (match) {
      const baseUuid = match[0]
      return `${baseUuid}_condicoes_gerais`
    }

    return `${documentId}_condicoes_gerais`
  }

  const buildDocList = (): { id: string; name: string; download_id: string }[] => {
    if (documents && documents.length > 0) {
      return documents
    }
    const list: { id: string; name: string; download_id: string }[] = [
      { id: 'quadro_resumo', name: 'Quadro Resumo (contrato principal)', download_id: documentId },
    ]
    const cg = getCondicoesGeraisId()
    if (cg) {
      list.push({ id: 'condicoes_gerais', name: 'Condições Gerais', download_id: cg })
    }
    return list
  }

  const docList = buildDocList()

  const fileSlug = (doc: DownloadInfo, format: DownloadFormat) => {
    const short = doc.download_id.slice(0, 8)
    if (doc.id === 'condicoes_gerais') {
      return `condicoes_gerais_${short}.${format === 'pdf' ? 'pdf' : 'docx'}`
    }
    return `contrato_${short}.${format === 'pdf' ? 'pdf' : 'docx'}`
  }

  const mimeFor = (format: DownloadFormat) =>
    format === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

  const handleDownload = async (doc: DownloadInfo, format: DownloadFormat) => {
    const key = `${doc.download_id}:${format}`
    try {
      setDownloadingKey(key)
      const response = await contractApi.downloadContract(doc.download_id, format)
      const blob = new Blob([response.data], { type: mimeFor(format) })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = fileSlug(doc, format)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error: any) {
      console.error('[DOWNLOAD]', error)
      alert(
        `Erro ao baixar o arquivo. Tente novamente.\n\nDetalhes: ${error.response?.data?.detail || error.message}`
      )
    } finally {
      setDownloadingKey(null)
    }
  }

  return (
    <div className="text-center py-8">
      <div className="mb-6">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-primary-600 mb-2">
          Contrato Gerado com Sucesso!
        </h2>
        <p className="text-subtitle">
          Baixe cada parte em <strong>PDF</strong> ou em <strong>Word (.docx)</strong>.
        </p>
      </div>

      <div className="space-y-6 max-w-md mx-auto text-left">
        {docList.map((doc) => (
          <div
            key={doc.id}
            className="border border-gray-200 rounded-lg p-4 bg-gray-50/80"
          >
            <h3 className="font-semibold text-primary-700 mb-3">{doc.name}</h3>
            <div className="flex flex-col sm:flex-row gap-2">
              <button
                type="button"
                onClick={() => handleDownload(doc, 'pdf')}
                disabled={downloadingKey !== null}
                className="flex-1 bg-primary-600 text-white py-2.5 px-4 rounded-lg text-sm font-medium
                  hover:bg-primary-700 disabled:bg-gray-400 transition-colors flex items-center justify-center gap-2"
              >
                {downloadingKey === `${doc.download_id}:pdf` ? (
                  <>
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Baixando...
                  </>
                ) : (
                  <>PDF</>
                )}
              </button>
              <button
                type="button"
                onClick={() => handleDownload(doc, 'docx')}
                disabled={downloadingKey !== null}
                className="flex-1 bg-white border border-primary-600 text-primary-600 py-2.5 px-4 rounded-lg text-sm font-medium
                  hover:bg-primary-50 disabled:bg-gray-100 disabled:border-gray-300 disabled:text-gray-400
                  transition-colors flex items-center justify-center gap-2"
              >
                {downloadingKey === `${doc.download_id}:docx` ? (
                  <>
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Baixando...
                  </>
                ) : (
                  <>Word</>
                )}
              </button>
            </div>
          </div>
        ))}
      </div>

      <button
        type="button"
        onClick={onReset}
        className="w-full max-w-xs mx-auto mt-8 bg-gray-200 text-gray-700 py-3 px-6 rounded-lg 
                   hover:bg-gray-300 transition-colors block"
      >
        Gerar Novo Contrato
      </button>

      <p className="mt-6 text-sm text-gray-500 text-center">
        O PDF preserva a formatação para leitura e arquivo. O Word permite ajustes finos no texto, se necessário.
      </p>
    </div>
  )
}
