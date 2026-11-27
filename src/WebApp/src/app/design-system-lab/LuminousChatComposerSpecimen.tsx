import { useEffect, useRef, useState } from 'react'
import { LuminousChatComposer } from '../../shared/design-system/patterns/LuminousChatComposer'
import type { LuminousChatAttachment } from '../../shared/design-system/patterns/LuminousChatComposer'
import { SectionHeader } from '../../shared/design-system/patterns/Panel'
import './luminous-chat-composer-specimen.css'

const exampleMessage = 'می‌توانید جزئیات منابع درآمد امسال را نشان دهید؟\nلطفاً آن‌ها را در یک جدول یا نمودار نمایش دهید.'

export function LuminousChatComposerSpecimen() {
  const [value, setValue] = useState('')
  const [attachments, setAttachments] = useState<readonly LuminousChatAttachment[]>([])
  const [processing, setProcessing] = useState(false)
  const [disabled, setDisabled] = useState(false)
  const [feedback, setFeedback] = useState('')
  const [submittedText, setSubmittedText] = useState('')
  const nextAttachmentId = useRef(0)
  const previewUrls = useRef(new Set<string>())

  useEffect(() => {
    const urls = previewUrls.current
    return () => {
      for (const url of urls) URL.revokeObjectURL(url)
      urls.clear()
    }
  }, [])

  function addFiles(files: readonly File[]) {
    const added = files.map((file): LuminousChatAttachment => {
      const id = `file-${nextAttachmentId.current++}`
      if (!file.type.startsWith('image/')) return { id, name: file.name }

      const imagePreviewUrl = URL.createObjectURL(file)
      previewUrls.current.add(imagePreviewUrl)
      return { id, name: file.name, imagePreviewUrl }
    })
    setAttachments((current) => [...current, ...added])
  }

  function removeAttachment(id: string) {
    const url = attachments.find((attachment) => attachment.id === id)?.imagePreviewUrl
    if (url) {
      URL.revokeObjectURL(url)
      previewUrls.current.delete(url)
    }
    setAttachments((current) => current.filter((attachment) => attachment.id !== id))
  }

  function clearDraft() {
    for (const url of previewUrls.current) URL.revokeObjectURL(url)
    previewUrls.current.clear()
    setAttachments([])
    setValue('')
  }

  function submitMessage(message: string, submittedAttachments: readonly LuminousChatAttachment[]) {
    clearDraft()
    setProcessing(true)
    setSubmittedText(message)
    const count = submittedAttachments.length
    setFeedback(count ? `پیام نمونه با ${count.toLocaleString('fa-IR')} پیوست ثبت شد.` : 'پیام نمونه ثبت شد.')
  }

  function finishResponse(result: 'complete' | 'stopped') {
    setProcessing(false)
    setFeedback(result === 'complete' ? 'پاسخ نمونه آماده است.' : 'تولید پاسخ نمونه متوقف شد.')
  }

  return (
    <section className="lab-composer-specimen" aria-labelledby="lab-composer-heading">
      <SectionHeader id="lab-composer-heading" level={2} title="کادر پیام گفت‌وگو" />
      <LuminousChatComposer
        value={value}
        attachments={attachments}
        processing={processing}
        disabled={disabled}
        onChange={setValue}
        onFilesSelected={addFiles}
        onRemoveAttachment={removeAttachment}
        onSubmit={submitMessage}
        onStop={() => finishResponse('stopped')}
      />
      <div className="lab-theme-control" role="group" aria-label="کنترل‌های نمونهٔ کادر پیام">
        <button type="button" onClick={() => setValue(exampleMessage)}>بارگذاری متن نمونه</button>
        <button type="button" onClick={clearDraft}>پاک کردن پیش‌نویس</button>
        <button type="button" aria-pressed={disabled} onClick={() => setDisabled(!disabled)}>
          غیرفعال کردن کادر پیام
        </button>
        {processing && <button type="button" onClick={() => finishResponse('complete')}>پایان پاسخ نمونه</button>}
      </div>
      <div className="lab-composer-feedback" role="status">{feedback}</div>
      {submittedText.trim() && (
        <p className="lab-composer-submission"><bdi>{submittedText}</bdi></p>
      )}
    </section>
  )
}
