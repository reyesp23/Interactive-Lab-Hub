//
//  Product.swift
//  Retailiot
//
//  Created by Patricio Reyes on 08/12/21.
//  Copyright © 2021 Apple. All rights reserved.
//

import Foundation
import UIKit

enum ProductSize {
    case small, medium, large
    
    var description: String {
        switch self {
        case .small: return "Small"
        case .medium: return "Medium"
        case .large: return "Large"
        }
    }
    
    var initial: String {
        return description.first?.uppercased() ?? ""
    }
}

enum ProductColor {
    case navy, mint, denim
    
    var color: UIColor {
        switch self {
        case .navy: return UIColor(red: 0.17, green: 0.20, blue: 0.29, alpha: 1.00)
        case .mint: return UIColor(red: 0.59, green: 0.65, blue: 0.54, alpha: 1.00)
        case .denim: return UIColor(red: 0.35, green: 0.49, blue: 0.67, alpha: 1.00)
        }
    }

    var description: String {
        switch self {
        case .navy: return "Navy blue"
        case .mint: return "Mint green"
        case .denim: return "Denim blue"
        }
    }
}

struct Product {
    var name: String
    var price: Double
    var color: ProductColor
    var size: ProductSize
    var image: UIImage?
    
    static let crewNeck = Product(name: "Crewneck Sweatshirt",
                                  price: 30.99,
                                  color: .mint,
                                  size: .small,
                                  image: UIImage(named: "pistachio.jpg"))
    
    static let basicShirt = Product(name: "Basic T-Shirt",
                                    price: 19.99,
                                    color: .navy,
                                    size: .small,
                                    image: UIImage(named: "navy.jpg"))
    
    static let denimShirt = Product(name: "Denim Shirt",
                                    price: 49.99,
                                    color: .denim,
                                    size: .large,
                                    image: UIImage(named: "denim.jpg"))
}
