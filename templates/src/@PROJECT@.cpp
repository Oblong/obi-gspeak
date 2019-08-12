#include <libLoam/c++/ArgParse.h>
#include <libLoam/c++/ObColor.h>
#include <libNoodoo/VisiDrome.h>
#include <libNoodoo/VisiFeld.h>

using namespace oblong::loam;
using namespace oblong::basement;
using namespace oblong::noodoo;

// Demo program to draw a different color on each feld,
// with a commandline argument to change which color it starts with.

ObColor palette[3] = {
  {0.7, 0.3, 0.3},
  {0.3, 0.7, 0.3},
  {0.3, 0.3, 0.7}
};

ArgParse::apint demo_shift;

ObRetort Setup (VFBunch *, Atmosphere *)
{
  const int N = VisiFeld::NumAllVisiFelds ();
  for (int i = 0; i < N; ++i)
    {
      VisiFeld *vf = VisiFeld::NthOfAllVisiFelds (i);
      const size_t palette_size = sizeof (palette) / sizeof (*palette);
      vf->SetBackgroundColor (palette[(i + demo_shift) % palette_size]);
    }
  return OB_OK;
}

int main (int argc, char **argv)
{
  ArgParse ap (argc, argv);
  ap.ArgInt ("demo-shift", "\aNumber of positions to shift palette",
             &demo_shift);
  ap.EasyFinish (0, ArgParse::UNLIMITED);

  // Pass any leftover commandline arguments to the VisiDrome constructor.
  // It will treat them as protein file names and deposit them into 'drome-pool',
  // which is like g-speak's live configuration inbox.
  // See e.g. "Setting up Screen and Feld Proteins" in
  // https://platform.oblong.com/learning/g-speak/recipes/

  VisiDrome *instance = new VisiDrome ("{{ project_name }}", ap.Leftovers ());

  instance->FindVFBunch ()->AppendPostFeldInfoHook (Setup);
  instance->Respire ();
  instance->Delete ();

  return 0;
}
