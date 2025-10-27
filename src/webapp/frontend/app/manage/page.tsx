import { Metadata } from 'next';
import ManageContent from '@/components/mixmeasureberry/ManageContent';

export const metadata: Metadata = {
  title: 'Manage Scale Recipes',
  description:
    'Select your MixMeasureBuddy scale and control which recipes sync to it.',
};

export default function ManagePage() {
  const backendTarget = process.env.NEXT_PUBLIC_BACKEND_URL;

  return (
    <ManageContent backendConfigured={Boolean(backendTarget)} />
  );
}
