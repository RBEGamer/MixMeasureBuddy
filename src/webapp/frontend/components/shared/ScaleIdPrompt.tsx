'use client';

import { useCallback } from 'react';
import { toast } from 'sonner';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/shared/ui/alert-dialog';
import { Input } from '@/components/shared/ui/input';
import { useScaleContext } from '@/context/scale-context';

export function ScaleIdPrompt(): JSX.Element {
  const {
    scaleId,
    promptOpen,
    closePrompt,
    declinePrompt,
    pendingScaleId,
    setPendingScaleId,
    confirmPendingScaleId,
  } = useScaleContext();

  const handleOpenChange = useCallback(
    (open: boolean) => {
      if (!open) {
        if (!scaleId) {
          declinePrompt();
        } else {
          closePrompt();
        }
      }
    },
    [scaleId, closePrompt, declinePrompt],
  );

  const handleConfirm = useCallback(() => {
    const result = confirmPendingScaleId();
    if (!result) {
      toast.error('Enter a scale ID to continue.');
      return;
    }
    toast.success(`Saved scale ID ${result}.`);
  }, [confirmPendingScaleId]);

  const handleDecline = useCallback(() => {
    declinePrompt();
    toast.info('You can set a scale ID later from any page.');
  }, [declinePrompt]);

  return (
    <AlertDialog open={promptOpen} onOpenChange={handleOpenChange}>
      <AlertDialogContent className="max-w-md">
        <AlertDialogHeader>
          <AlertDialogTitle>Connect to your MixMeasureBuddy</AlertDialogTitle>
          <AlertDialogDescription>
            Enter the system ID of the scale you want to manage. We&apos;ll remember it for next
            time.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <div className="space-y-3 py-2">
          <Input
            id="scale-id-prompt-input"
            placeholder="scale-1234"
            value={pendingScaleId}
            onChange={(event) => setPendingScaleId(event.target.value)}
          />
          <p className="text-xs text-muted-foreground">
            Don&apos;t have it handy? Choose &quot;Maybe later&quot; — you can set the scale ID at any
            time from Mix Lab, Manage, or the editor.
          </p>
        </div>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={handleDecline}>Maybe later</AlertDialogCancel>
          <AlertDialogAction onClick={handleConfirm}>Save ID</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
