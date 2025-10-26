import { NextResponse } from 'next/server';
import path from 'path';
import { promises as fs } from 'fs';

export const dynamic = 'force-dynamic';

const recipesDir = path.join(process.cwd(), 'src', 'recipes');

const sanitizeFileName = (fileName: string): string | null => {
  const decoded = decodeURIComponent(fileName);
  if (!/^[\w.-]+$/.test(decoded)) {
    return null;
  }
  if (!decoded.toLowerCase().endsWith('.recipe')) {
    return `${decoded}.recipe`;
  }
  return decoded;
};

export async function GET(
  _request: Request,
  { params }: { params: { systemId: string; recipeName: string } },
) {
  try {
    const safeFileName = sanitizeFileName(params.recipeName);
    if (!safeFileName) {
      return NextResponse.json({ error: 'Invalid recipe name.' }, { status: 400 });
    }

    const filePath = path.join(recipesDir, safeFileName);
    const file = await fs.readFile(filePath, 'utf8');
    const parsed = JSON.parse(file);

    return NextResponse.json({
      systemId: params.systemId,
      name: safeFileName.replace(/\.recipe$/i, ''),
      recipe: parsed,
    });
  } catch (error) {
    console.error(
      `[api][updater][recipe] Unable to read recipe ${params.recipeName}`,
      error,
    );
    return NextResponse.json(
      { error: 'Recipe not found.' },
      { status: 404 },
    );
  }
}
