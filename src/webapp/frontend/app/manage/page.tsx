import { Metadata } from 'next';
import SystemSelector from '@/components/mixmeasureberry/SystemSelector';
import RecipeAssignmentManager from '@/components/mixmeasureberry/RecipeAssignmentManager';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/shared/ui/card';
import { Badge } from '@/components/shared/ui/badge';

export const metadata: Metadata = {
  title: 'Manage Scale Recipes',
  description:
    'Select your MixMeasureBuddy scale and control which recipes sync to it.',
};

export default function ManagePage() {
  const backendTarget = process.env.NEXT_PUBLIC_BACKEND_URL;
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
        </section>

        {!backendTarget ? (
          <Card>
            <CardHeader>
              <CardTitle>Backend required</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3 text-sm text-muted-foreground">
              <p>
                Configure a backend by setting
                <Badge variant="outline" className="mx-2">NEXT_PUBLIC_BACKEND_URL</Badge>
                before building the frontend. The backend API must also expose
                the firmware-compatible updater routes.
              </p>
              <p>
                Once a backend is available, rebuild the frontend to unlock the
                management interface.
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
