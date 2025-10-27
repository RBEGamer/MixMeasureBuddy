'use client';

import SystemSelector from '@/components/mixmeasureberry/SystemSelector';
import RecipeAssignmentManager from '@/components/mixmeasureberry/RecipeAssignmentManager';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/shared/ui/card';
import { Badge } from '@/components/shared/ui/badge';
import { useBackendInfo, useBackendReachable } from '@/context/backend-context';

export default function ManageContent({
  backendConfigured,
}: {
  backendConfigured: boolean;
}) {
  const backendReachable = useBackendReachable();
  const { backendUrl } = useBackendInfo();
  const effectiveConfigured = backendConfigured || Boolean(backendUrl);

  return (
    <div className="w-full bg-gradient-to-b from-primary-100/30 to-transparent py-10 dark:from-primary-900/20">
      <div className="wide-container flex w-full flex-col gap-10">
        <section className="rounded-3xl bg-background/80 p-8 shadow-lg ring-1 ring-black/5 dark:bg-background/60">
          <h1 className="text-3xl font-semibold md:text-4xl">
            Manage your MixMeasureBuddy recipes
          </h1>
          <p className="mt-3 max-w-3xl text-base text-muted-foreground md:text-lg">
            Choose a scale ID, review which recipes are currently assigned, and
            add or remove entries from the bundled library so the firmware pulls
            exactly what you want.
          </p>
          {backendUrl && (
            <p className="mt-3 text-sm text-muted-foreground">
              Backend target: <Badge variant="outline">{backendUrl}</Badge>
            </p>
          )}
        </section>

        {!effectiveConfigured || !backendReachable ? (
          <Card>
            <CardHeader>
              <CardTitle>Backend required</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3 text-sm text-muted-foreground">
              <p>
                {effectiveConfigured
                  ? 'The backend is currently unreachable. Ensure it is running and accessible.'
                  : 'Configure NEXT_PUBLIC_BACKEND_URL (or expose your backend on port 4000) so the management interface can contact the API.'}
              </p>
              <p>
                Once the backend is online, the management tools will unlock automatically.
              </p>
            </CardContent>
          </Card>
        ) : (
          <SystemSelector>
            {(systemId) => <RecipeAssignmentManager systemId={systemId} />}
          </SystemSelector>
        )}
      </div>
    </div>
  );
}
