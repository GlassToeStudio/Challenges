using UnityEngine;

namespace GTS
{
    [ExecuteInEditMode]
    public class GaussBlur : MonoBehaviour
    {
        ///<summary>    Smoothing will increase the radius of the effected area.</summary>
        [Header("Adjust for increased effects")]
        [Range(0f, 1f)]public float smoothing = 1f;
        ///<summary>    The more passes, the more times the algorithm is ran on the render texture.</summary>
        [Range(1, 10)]public int passes = 1;

        ///<summary>    Will reduce the overall size of the image, thus reducing quality. Leaving a cheap blur effect.</summary>
        [Header("Cheap Quick Blur")]
        [Range(0f, 9f)]
        public int reduceImageSizeBy = 0;

        [Header("Material with GTS/GuassBlur Shader")]
        public Material blurMaterial;

        private int kernalValue = 0;

        private void GaussianBlur(RenderTexture source, RenderTexture destination)
        {
            RenderTexture renderTex = RenderTexture.GetTemporary(source.width, source.height, 0, source.format);

            for(int i = 0; i < passes; i++)
            {
                float radius = i * smoothing + smoothing;
                blurMaterial.SetFloat(GuassData._Radius, radius);
                Graphics.Blit(source, renderTex, blurMaterial, 1 + kernalValue);
                source.DiscardContents();

                if(i == passes - 1)
                    Graphics.Blit(renderTex, destination, blurMaterial, 2 + kernalValue);
                else
                {
                    Graphics.Blit(renderTex, source, blurMaterial, 2 + kernalValue);
                    renderTex.DiscardContents();
                }
            }
            RenderTexture.ReleaseTemporary(renderTex);
        }

        private void OnRenderImage(RenderTexture source, RenderTexture destination)
        {
            int width = source.width >> reduceImageSizeBy;
            int height = source.height >> reduceImageSizeBy;

            RenderTexture renderTex = RenderTexture.GetTemporary(width, height, 0, source.format);
            Graphics.Blit(source, renderTex);
            GaussianBlur(renderTex, destination);
            RenderTexture.ReleaseTemporary(renderTex);
        }

        // Guess this is the only way to get the _Radius...
        protected static class GuassData
        {
            public static readonly int _Radius = Shader.PropertyToID("_Radius");
        }
    }
}