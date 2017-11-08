// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "GTS/Gaussian_Blur"
{
	Properties
	{
		_MainTex ("", 2D) = "white" {}
	}

	CGINCLUDE

	#include "UnityCG.cginc"

	struct appdata
	{
		float4 vertex : POSITION;
		float2 uv : TEXCOORD0;
	};

	struct v2f
	{
		float4 vertex : SV_POSITION;
		float2 uv : TEXCOORD0;
	};

	struct gauss_data
	{
		float4 vertex : SV_POSITION;
		float2 uv : TEXCOORD0;
		float4 coords[2] : TEXCOORD1;
	};

	uniform sampler2D _MainTex;
	uniform float2 _MainTex_TexelSize;
    uniform float2 _RenderedScene_TexelSize;

	uniform float _Radius;


	v2f vert (appdata v)
	{
        v2f o;
        o.vertex = UnityObjectToClipPos(v.vertex);
        o.uv = v.uv;
        return o;
	}

	fixed4 frag (v2f i) : SV_Target
	{
		fixed3 color = tex2D(_MainTex, i.uv);
		return fixed4(color, 1.0);
	}

    gauss_data gauss_h (appdata v)
	{
		gauss_data gd;
		float2 offset1 = float2(_MainTex_TexelSize.x * _Radius * 1.38461538, 0.0); 
		float2 offset2 = float2(_MainTex_TexelSize.x * _Radius * 3.23076923, 0.0);

        gd.vertex = UnityObjectToClipPos(v.vertex);
        gd.uv.xy = v.uv.xy;

        gd.coords[0].xy = gd.uv + offset1;
        gd.coords[0].zw = gd.uv - offset1;
        gd.coords[1].xy = gd.uv + offset2;
        gd.coords[1].zw = gd.uv - offset2;

		return gd;
	}

	gauss_data gauss_v (appdata v)
	{
		gauss_data gd;
		float2 offset1 = float2(0.0, _MainTex_TexelSize.y * _Radius * 1.38461538); 
		float2 offset2 = float2(0.0, _MainTex_TexelSize.y * _Radius * 3.23076923);

		gd.vertex = UnityObjectToClipPos(v.vertex);
		gd.uv.xy = v.uv.xy;

		gd.coords[0].xy = gd.uv + offset1;
		gd.coords[0].zw = gd.uv - offset1;
		gd.coords[1].xy = gd.uv + offset2;
		gd.coords[1].zw = gd.uv - offset2;

		return gd;
	}

	fixed4 gauss_frag (gauss_data gd) : SV_Target
	{
		fixed3 sum = tex2D(_MainTex, gd.uv).xyz * 0.22702702;
		sum += tex2D(_MainTex, gd.coords[0].xy).xyz * 0.31621621;
		sum += tex2D(_MainTex, gd.coords[0].zw).xyz * 0.31621621;
		sum += tex2D(_MainTex, gd.coords[1].xy).xyz * 0.07027027;
		sum += tex2D(_MainTex, gd.coords[1].zw).xyz * 0.07027027;
		return fixed4(sum, 1.0);
	}

	ENDCG

	SubShader
	{
		Pass{
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			ENDCG
		}

		Pass{
			CGPROGRAM
			#pragma vertex gauss_v
			#pragma fragment gauss_frag
			ENDCG
		}

		Pass{
			CGPROGRAM
			#pragma vertex gauss_h
			#pragma fragment gauss_frag
			ENDCG
		}

	}
}
