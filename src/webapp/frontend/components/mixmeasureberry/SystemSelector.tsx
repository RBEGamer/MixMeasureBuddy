'use client';

import { useState } from 'react';
import { Input } from '@/components/shared/ui/input';
import { Button } from '@/components/shared/ui/button';

export default function SystemSelector({
  children,
}: {
  children: (systemId: string) => React.ReactNode;
}) {
  const [submittedId, setSubmittedId] = useState<string>('');
  const [inputValue, setInputValue] = useState<string>('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!inputValue.trim().length) {
      return;
    }
    setSubmittedId(inputValue.trim());
  };

  return (
    <div className="flex w-full flex-col gap-6">
      <form
        onSubmit={handleSubmit}
        className="flex w-full flex-col gap-3 rounded-2xl border border-dashed border-primary-200/60 bg-background p-6 shadow-sm dark:border-primary-800/60"
      >
        <label htmlFor="system-id-input" className="text-sm font-medium text-muted-foreground">
          Enter scale ID
        </label>
        <div className="flex flex-col gap-3 sm:flex-row">
          <Input
            id="system-id-input"
            value={inputValue}
            onChange={(event) => setInputValue(event.target.value)}
            placeholder="e.g. scale-1234"
            className="sm:max-w-xs"
          />
          <Button type="submit" className="sm:w-40">
            Manage recipes
          </Button>
        </div>
        <p className="text-xs text-muted-foreground">
          Your scale ID is the identifier used by the firmware when checking for
          updates (see `NETWORK_API_ENPOINT`).
        </p>
      </form>

      {submittedId && (
        <section className="rounded-2xl border border-primary-100/80 bg-white/80 p-6 shadow dark:border-primary-900/50 dark:bg-slate-950/60">
          {children(submittedId)}
        </section>
      )}
    </div>
  );
}
