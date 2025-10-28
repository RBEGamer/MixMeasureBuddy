'use client';

import { useEffect } from 'react';
import { Button } from '@/components/shared/ui/button';
import { Badge } from '@/components/shared/ui/badge';
import { useScaleContext } from '@/context/scale-context';

export default function SystemSelector({
  children,
}: {
  children: (systemId: string) => React.ReactNode;
}) {
  const {
    scaleId,
    clearScaleId,
    declinedPrompts,
    openPrompt,
    promptOpen,
  } = useScaleContext();

  useEffect(() => {
    if (!scaleId && !declinedPrompts && !promptOpen) {
      openPrompt();
    }
  }, [scaleId, declinedPrompts, promptOpen, openPrompt]);

  return (
    <div className="flex w-full flex-col gap-6">
      <section className="flex w-full flex-col gap-4 rounded-2xl border border-dashed border-primary-200/60 bg-background p-6 shadow-sm dark:border-primary-800/60">
        <div className="flex flex-col gap-2">
          <span className="text-sm font-medium text-muted-foreground">Scale selection</span>
          <p className="text-xs text-muted-foreground">
            Your scale ID is the identifier the firmware uses when checking for recipe updates (see
            <code className="mx-1 rounded bg-muted px-1 py-0.5 text-[0.7rem]">NETWORK_API_ENPOINT</code>
            in the config).
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <Badge variant="outline">
            {scaleId ? `Scale ID: ${scaleId}` : 'No scale ID saved'}
          </Badge>
          <div className="flex flex-wrap items-center gap-2">
            <Button type="button" onClick={() => openPrompt(scaleId)}>
              {scaleId ? 'Change scale ID' : 'Set scale ID'}
            </Button>
            {scaleId && (
              <Button type="button" variant="ghost" onClick={clearScaleId}>
                Clear
              </Button>
            )}
          </div>
        </div>
      </section>

      {scaleId ? (
        <section className="rounded-2xl border border-primary-100/80 bg-white/80 p-6 shadow dark:border-primary-900/50 dark:bg-slate-950/60">
          {children(scaleId)}
        </section>
      ) : (
        <div className="rounded-2xl border border-dashed bg-muted/30 p-6 text-sm text-muted-foreground">
          Set a scale ID to review assignments and custom recipes.
        </div>
      )}
    </div>
  );
}
