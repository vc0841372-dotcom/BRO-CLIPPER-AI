package com.broclipper.ai

import android.app.Activity
import android.os.Bundle
import android.graphics.Color
import android.view.Gravity
import android.widget.*
import android.view.ViewGroup
import android.text.InputType

class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(28, 35, 28, 35)
            setBackgroundColor(Color.rgb(15, 18, 28))
        }

        val title = TextView(this).apply {
            text = "BRO CLIPPER AI"
            textSize = 28f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
        }

        val subtitle = TextView(this).apply {
            text = "Convierte videos en clips"
            textSize = 16f
            setTextColor(Color.LTGRAY)
            gravity = Gravity.CENTER
        }

        val link = EditText(this).apply {
            hint = "Pega aquí el enlace de YouTube"
            inputType = InputType.TYPE_TEXT_VARIATION_URI
            setSingleLine(true)
            setPadding(16, 16, 16, 16)
        }

        val button = Button(this).apply {
            text = "ANALIZAR Y CREAR 3 CLIPS"
        }

        val status = TextView(this).apply {
            text = "Listo para comenzar"
            textSize = 15f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
        }

        button.setOnClickListener {
            val url = link.text.toString().trim()
            if (!url.startsWith("https://www.youtube.com/") &&
                !url.startsWith("https://youtu.be/")) {
                status.text = "Pega un enlace válido de YouTube."
            } else {
                status.text = "Enlace recibido. El motor de clips todavía debe integrarse."
            }
        }

        layout.addView(title)
        layout.addView(subtitle)
        layout.addView(link, LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
        ).apply { topMargin = 35 })
        layout.addView(button)
        layout.addView(status)

        setContentView(layout)
    }
}
