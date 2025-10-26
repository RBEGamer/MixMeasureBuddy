import { NextResponse } from 'next/server';
import path from 'path';
import { promises as fs } from 'fs';

export const dynamic = 'force-dynamic';

const recipesDir = path.join(process.cwd(), 'src', 'recipes');

export async function GET(
  _request: Request,
  { params }: { params: { systemId: string } },
) {
  try {
    const files = await fs.readdir(recipesDir);
    const recipeFiles = files.filter((file) =>
      file.toLowerCase().endsWith('.recipe'),
    );
    return NextResponse.json({
      systemId: params.systemId,
      recipes: recipeFiles,
    });
  } catch (error) {
    console.error('[api][updater][recipes] Failed to read recipes', error);
    return NextResponse.json(
      { error: 'Failed to read recipe directory.' },
      { status: 500 },
    );
  }
}

