'use client'

import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X, CheckCircle, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { api } from '@/lib/api'

interface ManuscriptUploaderProps {
  worldId: string
  onUploadComplete?: (manuscript: any) => void
}

type UploadStatus = 'idle' | 'uploading' | 'success' | 'error'

export const ManuscriptUploader: React.FC<ManuscriptUploaderProps> = ({
  worldId,
  onUploadComplete
}) => {
  const [status, setStatus] = useState<UploadStatus>('idle')
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [errorMessage, setErrorMessage] = useState<string>('')

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return
    
    const file = acceptedFiles[0]
    
    // Validate file type
    const validTypes = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    const fileExtension = file.name.split('.').pop()?.toLowerCase()
    const validExtensions = ['txt', 'pdf', 'docx']
    
    if (!validExtensions.includes(fileExtension || '')) {
      setStatus('error')
      setErrorMessage('Invalid file type. Please upload TXT, PDF, or DOCX files.')
      return
    }
    
    // Validate file size (50MB max)
    const maxSize = 50 * 1024 * 1024
    if (file.size > maxSize) {
      setStatus('error')
      setErrorMessage('File size exceeds 50MB limit.')
      return
    }
    
    setUploadedFile(file)
    setStatus('uploading')
    
    try {
      const manuscript = await api.manuscripts.upload(worldId, file)
      setStatus('success')
      onUploadComplete?.(manuscript)
    } catch (error: any) {
      setStatus('error')
      setErrorMessage(error.message || 'Upload failed. Please try again.')
    }
  }, [worldId, onUploadComplete])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1,
    disabled: status === 'uploading' || status === 'success'
  })

  const handleReset = () => {
    setStatus('idle')
    setUploadedFile(null)
    setErrorMessage('')
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={cn(
          "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
          isDragActive && "border-primary bg-primary/5",
          status === 'error' && "border-destructive bg-destructive/5",
          status === 'success' && "border-green-500 bg-green-50",
          (status === 'uploading' || status === 'success') && "cursor-default"
        )}
      >
        <input {...getInputProps()} />
        
        {status === 'idle' && (
          <>
            <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">
              {isDragActive ? 'Drop your manuscript here' : 'Upload your manuscript'}
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Drag and drop your file here, or click to browse
            </p>
            <p className="text-xs text-muted-foreground">
              Supported formats: TXT, PDF, DOCX (max 50MB)
            </p>
          </>
        )}
        
        {status === 'uploading' && (
          <>
            <FileText className="mx-auto h-12 w-12 text-primary mb-4 animate-pulse" />
            <h3 className="text-lg font-semibold mb-2">Uploading...</h3>
            <p className="text-sm text-muted-foreground">{uploadedFile?.name}</p>
          </>
        )}
        
        {status === 'success' && (
          <>
            <CheckCircle className="mx-auto h-12 w-12 text-green-500 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Upload successful!</h3>
            <p className="text-sm text-muted-foreground mb-4">{uploadedFile?.name}</p>
            <Button variant="outline" size="sm" onClick={handleReset}>
              Upload another file
            </Button>
          </>
        )}
        
        {status === 'error' && (
          <>
            <AlertCircle className="mx-auto h-12 w-12 text-destructive mb-4" />
            <h3 className="text-lg font-semibold mb-2">Upload failed</h3>
            <p className="text-sm text-destructive mb-4">{errorMessage}</p>
            <Button variant="outline" size="sm" onClick={handleReset}>
              Try again
            </Button>
          </>
        )}
      </div>
    </div>
  )
}

export default ManuscriptUploader
