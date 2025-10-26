import { NextResponse } from 'next/server';
import path from 'path';
import { promises as fs } from 'fs';

export const dynamic = 'force-dynamic';

const recipesDir = path.join(process.cwd(), 'src', 'recipes');

const countRecipeFiles = async (): Promise<number> => {
  try {
    const files = await fs.readdir(recipesDir);
    return files.filter((file) => file.toLowerCase().endsWith('.recipe'))
      .length;
  } catch (error) {
    console.error('[api][updater][countRecipeFiles]', error);
    return 0;
  }
};

export async function GET(
  _request: Request,
  { params }: { params: { systemId: string } },
) {
  const totalRecipes = await countRecipeFiles();

  return NextResponse.json({
    status: 'ok',
    systemId: params.systemId,
    totalRecipes,
    generatedAt: new Date().toISOString(),
  });
}

