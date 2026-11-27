import { useRef } from 'react'
import type { ChangeEvent, FormEvent, KeyboardEvent, MouseEvent } from 'react'
import './luminous-chat-composer.css'

export type LuminousChatAttachment = {
  id: string
  name: string
  imagePreviewUrl?: string
}

export type LuminousChatComposerProps = {
  value: string
  attachments: readonly LuminousChatAttachment[]
  placeholder?: string
  accept?: string
  disabled?: boolean
  processing?: boolean
  onChange: (value: string) => void
  onFilesSelected: (files: readonly File[]) => void
  onRemoveAttachment: (id: string) => void
  onSubmit: (value: string, attachments: readonly LuminousChatAttachment[]) => void
  onStop: () => void
}

export function LuminousChatComposer({
  value,
  attachments,
  placeholder = 'پیام خود را بنویسید…',
  accept,
  disabled = false,
  processing = false,
  onChange,
  onFilesSelected,
  onRemoveAttachment,
  onSubmit,
  onStop,
}: LuminousChatComposerProps) {
  const editor = useRef<HTMLTextAreaElement>(null)
  const picker = useRef<HTMLInputElement>(null)
  const attachButton = useRef<HTMLButtonElement>(null)
  const composing = useRef(false)
  const canSubmit = !disabled && !processing && (value.trim().length > 0 || attachments.length > 0)

  function submitDraft() {
    if (!canSubmit || composing.current) return

    onSubmit(value, attachments)
    editor.current?.focus()
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    submitDraft()
  }

  function focusEditorFromSurface(event: MouseEvent<HTMLFormElement>) {
    const target = event.target
    if (!disabled && target instanceof Element && !target.closest('textarea, button, input')) {
      editor.current?.focus()
    }
  }

  function handleEditorKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key !== 'Enter' || event.shiftKey || event.altKey || event.ctrlKey || event.metaKey) return
    // Some browsers report the IME commit as key code 229 after compositionend.
    if (composing.current || event.nativeEvent.isComposing || event.nativeEvent.keyCode === 229) return

    event.preventDefault()
    if (!event.repeat) submitDraft()
  }

  function handleFiles(event: ChangeEvent<HTMLInputElement>) {
    const files = Array.from(event.currentTarget.files ?? [])
    event.currentTarget.value = ''
    if (files.length > 0) onFilesSelected(files)
  }

  function removeAttachment(id: string) {
    onRemoveAttachment(id)
    attachButton.current?.focus()
  }

  function stopGeneration(event: MouseEvent<HTMLButtonElement>) {
    // The control can become a submit button before the click completes.
    event.preventDefault()
    onStop()
    editor.current?.focus()
  }

  return (
    <div className="didrah-chat-composer" lang="fa" dir="rtl">
      <form
        className="didrah-composer-form"
        aria-label="نوشتن پیام"
        data-disabled={disabled}
        onClick={focusEditorFromSurface}
        onSubmit={handleSubmit}
      >
        <div className="didrah-composer-editor" data-value={value}>
          <textarea
            ref={editor}
            className="didrah-composer-message"
            aria-label="متن پیام"
            rows={2}
            placeholder={placeholder}
            value={value}
            disabled={disabled}
            onChange={(event) => onChange(event.currentTarget.value)}
            onKeyDown={handleEditorKeyDown}
            onCompositionStart={() => { composing.current = true }}
            onCompositionEnd={() => { composing.current = false }}
            onBlur={() => { composing.current = false }}
          />
        </div>
        {attachments.length > 0 && (
          <ul className="didrah-composer-attachments" aria-label="پیوست‌ها">
            {attachments.map(({ id, name, imagePreviewUrl }) => (
              <li key={id} className="didrah-composer-file">
                {imagePreviewUrl && (
                  <img key={imagePreviewUrl} src={imagePreviewUrl} alt="" onError={(event) => { event.currentTarget.hidden = true }} />
                )}
                <bdi title={name}>{name}</bdi>
                <button
                  type="button"
                  className="didrah-composer-remove"
                  aria-label={`حذف پیوست ${name}`}
                  disabled={disabled}
                  onClick={() => removeAttachment(id)}
                >
                  <svg viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <path d="m4 4 8 8m0-8-8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                </button>
              </li>
            ))}
          </ul>
        )}
        <div className="didrah-composer-actions">
          <button
            ref={attachButton}
            className="didrah-composer-attach"
            type="button"
            aria-label="افزودن پیوست"
            disabled={disabled}
            onClick={() => picker.current?.click()}
          >
            <svg viewBox="0 0 40 40" fill="none" aria-hidden="true">
              <path
                d="M32.3 20.5 20 32.8c-3.7 3.7-8.1 3.5-11.3.3-3.2-3.1-3.5-7.3 0-10.8L24.1 6.9c2.2-2.2 5.1-2.4 7.1-.4 2.1 2 2 5-.1 7.1L15.9 29c-1.1 1.1-2.5 1.2-3.5.2s-1-2.5.1-3.6l12.4-12.5"
                stroke="currentColor"
                strokeWidth="2.7"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
          <input ref={picker} type="file" accept={accept} multiple hidden disabled={disabled} onChange={handleFiles} />
          <button
            className="didrah-composer-send"
            type={processing ? 'button' : 'submit'}
            aria-label={processing ? 'توقف تولید پاسخ' : 'ارسال پیام'}
            disabled={disabled || (!processing && !canSubmit)}
            onClick={processing ? stopGeneration : undefined}
          >
            <svg viewBox="0 0 40 40" fill="none" aria-hidden="true">
              {processing ? (
                <rect x="10" y="10" width="20" height="20" rx="3" fill="currentColor" />
              ) : (
                <>
                  <path
                    d="M8.5 7.5 35.1 20.3 8.5 32.9l4.6-12.6L8.5 7.5Zm4.6 12.8h22"
                    stroke="currentColor"
                    strokeWidth="2.55"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path d="M32.7 2.7c.5 2.9 2.1 4.5 5 5.1-2.9.5-4.5 2.1-5 5-.6-2.9-2.2-4.5-5.1-5 2.9-.6 4.5-2.2 5.1-5.1Z" fill="currentColor" />
                </>
              )}
            </svg>
          </button>
        </div>
        <span className="didrah-composer-status" role="status">
          {processing ? 'در حال تولید پاسخ…' : ''}
        </span>
      </form>
    </div>
  )
}
